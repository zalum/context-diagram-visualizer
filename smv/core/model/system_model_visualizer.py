from sms import schemas
from sms import relations as relation_types
from smv.core.model import system_model as sm


class component_model_visualizer:

  def __init__(self, system_model: sm.component_model):
      self.system_model = system_model

  def draw(self):
      orphanApplications = self.system_model.get_orphan_applications()
      lines = ["@startuml","left to right direction"]
      [lines.extend(self._drawProduct(vertex)) for vertex in self.system_model.getProducts()]
      lines.extend([self._drawEdges(edge) for edge in self.system_model.get_calling_relations()])
      lines.extend([self._drawApplication(vertex) for vertex in orphanApplications])
      lines.append("@enduml")
      return lines

  def _drawProduct(self,product):
      applications = self.system_model.get_applications_in_product(product)
      drawnProudct = ["folder %s{"%self._drawProductName(product)]
      drawnProudct.extend([self._drawApplication(application) for application in applications])
      drawnProudct.append("}")
      return drawnProudct

  def _drawApplication(self, application):
      return self._drawApplicationByName(self.system_model.get_component_name(application))
  def _drawProductName(self,product):
      return self.system_model.get_component_name(product).replace(" ", "_")
  def _drawApplicationByVertex(self,vertex):
      return self._drawApplicationByName(self.system_model.get_component_name(vertex))
  def _drawApplicationByName(self,name):
      return "[%s]"%name
  def _drawEdges(self,edge):
      return "[%s]-->[%s]"%(self.system_model.get_component_name(edge["start"]),\
                            self.system_model.get_component_name(edge["end"]))

class datamodel_visualizer():
    def __init__(self, system_model: sm.data_model):
        self.system_model = system_model

    def draw(self, collapsed_columns = False):
        lines = ["@startuml","left to right direction"]
        self.draw_database_users(collapsed_columns, lines)
        self.draw_foreign_keys(collapsed_columns, lines)
        self._draw_composition_relations(collapsed_columns, lines)
        lines.append("@enduml")
        return lines

    def draw_foreign_keys(self, colapsed_columns, lines):
        [lines.extend(self._draw_foreign_key(fk, colapsed_columns)) for fk in self.system_model.get_foreign_keys()]

    def draw_database_users(self, colapsed_columns, lines):
        [lines.extend(self._draw_database_user(schema, colapsed_columns)) for schema in
         self.system_model.get_database_users()]

    def _draw_database_user(self, database_user, colapsed_columns = False):
        tables = self.system_model.get_tables_in_database_user(database_user)
        drawn_schema = ["package \"%s\"{" % database_user]
        [drawn_schema.extend(self._draw_table(table,colapsed_columns)) for table in tables]
        drawn_schema.append("}")
        return drawn_schema

    def _draw_table(self, table,colapsed_columns=False):
        table_vertex = self.system_model.get_system_node(table)
        if "name" in table_vertex:
            drawn_table = ["class \"{}\" as {} {{".format(table_vertex["name"],table)]
        else:
            drawn_table = ["class {} {{".format(table)]
        columns = self.system_model.get_columns_in_table(table)
        if colapsed_columns == False:
            [drawn_table.extend(self._draw_column(column)) for column in columns]
        drawn_table.extend("}")
        return drawn_table

    def _draw_column(self, column):
        return ["+ %s"%column]

    def _draw_foreign_key_between_tables(self, fk):
        return ["%s --> %s : %s::%s"% \
                (fk["start"]["table"],
                 fk["end"]["table"],
                 fk["start"]["column"],
                 fk["end"]["column"])]

    def _draw_foreign_key_between_columns(self, fk):
        return ["%s::%s --> %s::%s"% \
        (fk["start"]["table"],
         fk["start"]["column"],
         fk["end"]["table"],
         fk["end"]["column"])]

    def _draw_foreign_key(self, fk, colapsed_columns):
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

    def _draw_composition_relations(self, collapsed_columns, lines):
        relations = self.system_model.get_relations_of_type(relation_types.composition)
        for relation in relations:
            self._draw_composition_relation(collapsed_columns, relation, lines)

    def _draw_composition_relation(self, collapsed_columns, relation, lines):
        start_node = relation["start"]
        end_node = relation["end"]
        start_node_name = self._draw_node_for_relation(start_node, collapsed_columns)
        end_node_name = self._draw_node_for_relation(end_node, collapsed_columns)
        lines.append("{} --* {}".format(start_node_name, end_node_name))



