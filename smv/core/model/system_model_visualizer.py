from sms import schemas, nodes, relations
from sms import relations as relation_types
from smv.core.model import system_model as sm
from smv.core.model.system_model import data_model, system_model


class PlatnumlDiagram:
    def __init__(self, lines: [] = None):
        if lines is None:
            self.lines = []
        else:
            self.lines = lines  # type: []

    def add_front(self, part: []):
        start_index = self.__get_start_index()
        for line in part:
            self.lines.insert(start_index, line)
            start_index += 1

    def __get_start_index(self):
        if len(self.lines) == 0:
            return 0
        if self.lines[0].startswith("@startuml"):
            return 2
        return 0

    def append(self, part):
        self.lines.extend(part)


class ComponentModelVisualizer:

    def __init__(self, system_model: sm.component_model):
        self.system_model = system_model

    def draw(self):
        orphanApplications = self.system_model.get_orphan_applications()
        lines = ["@startuml", "left to right direction"]
        [lines.extend(self._drawProduct(vertex)) for vertex in self.system_model.getProducts()]
        lines.extend([self._drawEdges(edge) for edge in self.system_model.get_calling_relations()])
        lines.extend([self._drawApplication(vertex) for vertex in orphanApplications])
        lines.append("@enduml")
        return lines

    def _drawProduct(self, product):
        applications = self.system_model.get_applications_in_product(product)
        drawnProudct = ["folder %s{" % self._drawProductName(product)]
        drawnProudct.extend([self._drawApplication(application) for application in applications])
        drawnProudct.append("}")
        return drawnProudct

    def _drawApplication(self, application):
        return self._drawApplicationByName(self.system_model.get_component_name(application))

    def _drawProductName(self, product):
        return self.system_model.get_component_name(product).replace(" ", "_")

    def _drawApplicationByVertex(self, vertex):
        return self._drawApplicationByName(self.system_model.get_component_name(vertex))

    def _drawApplicationByName(self, name):
        return "[%s]" % name

    def _drawEdges(self, edge):
        return "[%s]-->[%s]" % (self.system_model.get_component_name(edge["start"]), \
                                self.system_model.get_component_name(edge["end"]))


class DatamodelVisualizer():
    def __init__(self, system_model: sm.data_model):
        self.system_model = system_model

    def draw(self, database_user=None, collapsed_columns=False) -> []:
        diagram = PlatnumlDiagram()
        diagram.append(["@startuml", "left to right direction"])
        diagram.append(self.__draw_database_users(database_user, collapsed_columns))
        diagram.append(self.__draw_foreign_keys(collapsed_columns))
        diagram.append(self.__draw_composition_relations(collapsed_columns))
        diagram.append(["@enduml"])
        return diagram.lines

    def __draw_foreign_keys(self, colapsed_columns):
        part = PlatnumlDiagram()
        for fk in self.system_model.get_foreign_keys():
            part.append(self.__draw_foreign_key(fk, colapsed_columns))
        return part.lines

    def __draw_database_users(self, focus_database_user=None, colapsed_columns=False):
        part = PlatnumlDiagram()
        for database_user in self.system_model.get_database_users():
            part.append(self.__draw_database_user(database_user, focus_database_user, colapsed_columns))
        return part.lines

    def __draw_database_user(self, database_user, focus_database_user, colapsed_columns=False):
        tables = self.system_model.get_tables_in_database_user(database_user)
        if len(tables) == 0 and database_user == focus_database_user and focus_database_user is not None:
            return []
        database_user_diagram = PlatnumlDiagram()
        database_user_diagram.append(["package \"%s\"{" % database_user])
        for table in tables:
            accessors = self.__get_table_privileges(focus_database_user, table)
            table_diagram = self.draw_table(table, accessors=accessors, colapsed_columns=colapsed_columns)
            database_user_diagram.append(table_diagram)
        database_user_diagram.append(["}"])
        return database_user_diagram.lines

    def __get_table_privileges(self, bounded_context, table):
        accessors = []
        relations_types = self.system_model.get_relation_types_between(bounded_context, table)
        for relation_type in relations_types:
            if self.__is_privilege_relation(relation_type):
                accessors.extend(relation_type[0])
        return accessors

    def draw_table(self, table, accessors=[], colapsed_columns=False):
        table_vertex = self.system_model.get_system_node(table)
        if "name" in table_vertex:
            drawn_table = ["class \"{}\" as {} {{".format(table_vertex["name"], table)]
        else:
            drawn_table = ["class {} {{".format(table)]
        drawn_table.extend(self.__draw_table_accessors(accessors))
        columns = self.system_model.get_columns_in_table(table)
        if colapsed_columns == False:
            [drawn_table.extend(self._draw_column(column)) for column in columns]
        drawn_table.extend("}")
        return drawn_table

    def _draw_column(self, column):
        return ["+ %s" % column]

    def _draw_foreign_key_between_tables(self, fk):
        return ["%s --> %s : %s::%s" % \
                (fk["start"]["table"],
                 fk["end"]["table"],
                 fk["start"]["column"],
                 fk["end"]["column"])]

    def _draw_foreign_key_between_columns(self, fk):
        return ["%s::%s --> %s::%s" % \
                (fk["start"]["table"],
                 fk["start"]["column"],
                 fk["end"]["table"],
                 fk["end"]["column"])]

    def __draw_foreign_key(self, fk, colapsed_columns):
        if colapsed_columns == True:
            return self._draw_foreign_key_between_tables(fk)
        return self._draw_foreign_key_between_columns(fk)

    def _draw_node_for_relation(self, system_node, collapsed_columns):
        if self.system_model.is_system_node_of_type(system_node, schemas.datamodel.nodes.column):
            end_table = self.system_model.get_table_for_column(system_node)
            if collapsed_columns:
                return end_table
            else:
                return "{}::{}".format(end_table, system_node)
        else:
            return system_node

    def __draw_composition_relations(self, collapsed_columns):
        part = PlatnumlDiagram()
        relations = self.system_model.get_relations_of_type(relation_types.composition)
        for relation in relations:
            part.append(self.__draw_composition_relation(collapsed_columns, relation))
        return part.lines

    def __draw_composition_relation(self, collapsed_columns, relation):
        start_node = relation["start"]
        end_node = relation["end"]
        start_node_name = self._draw_node_for_relation(start_node, collapsed_columns)
        end_node_name = self._draw_node_for_relation(end_node, collapsed_columns)
        return ["{} --* {}".format(start_node_name, end_node_name)]

    @staticmethod
    def __draw_table_accessors(accessors):
        lines = []
        if accessors is None or len(accessors) == 0:
            return lines
        lines.append("..access..")
        lines.append(" / ".join(accessors))
        lines.append("__")
        return lines

    @staticmethod
    def __is_privilege_relation(relation_type):
        return relation_type in [relations.reads, relations.writes, relations.deletes]


class BoundedContextVisualizer:
    def __init__(self, system_model: sm.data_model):
        self.system_model = system_model
        datamodel = data_model(self.system_model.graph)
        self.datamodel_visualizer = DatamodelVisualizer(datamodel)

    def draw(self, bounded_context):
        diagram = PlatnumlDiagram(self.datamodel_visualizer.draw())
        title = [self.__draw_title(bounded_context)]
        tables = self.__draw_tables(bounded_context)
        diagram.add_front(tables)
        diagram.add_front(title)
        return diagram.lines

    def __draw_title(self, bounded_context):
        return "title '{}' Bounded Context".format(bounded_context)

    def __draw_tables(self, bounded_context):
        tables = set(self.system_model.get_children(bounded_context, of_type=nodes.table))
        diagram = PlatnumlDiagram()
        for table in tables:
            accessors = self.__get_table_access(bounded_context, table)
            table_diagram_part = self.datamodel_visualizer.draw_table(table, accessors=accessors)
            diagram.add_front(table_diagram_part)
        return diagram.lines

    def __get_table_access(self, bounded_context, table):
        accessors = []
        relations_types = self.system_model.get_relation_types_between(bounded_context, table)
        for relation_type in relations_types:
            if self.__is_accessor_relation(relation_type):
                accessors.extend(relation_type[0])
        return accessors

    @staticmethod
    def __is_accessor_relation(relation_type):
        return relation_type in [relations.writes, relations.reads]
