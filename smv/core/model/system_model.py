import json
from smv.core import Response
from smv.core import RESPONSE_OK
from smv.core import RESPONSE_ERROR


def empty_graph():
    return {SYSTEM_NODES: {}, RELATIONS: []}

RESPONSE_OK_deprecated = object()
SYSTEM_NODES = "system-nodes"
RELATIONS = "relations"
SYSTEM_NODE_TYPE = "type"
RELATION_TYPE = "relation-type"

class DatamodelRelationTypes():
    fk = "fk"
    composition = "composition"
    contains = "contains"
    owns = "owns"
    uses = "uses"

class RelationTypes():
    datamodel = DatamodelRelationTypes

class DatamodelNodeTypes:
    table = "table"
    column = "column"
    database_user = "database-user"

class SystemNodesTypes():
    datamodel = DatamodelNodeTypes


class system_model:
    def __init__(self, graphx=None):
        if graphx is None or len(graphx.keys()) == 0:
            self.graph = empty_graph()
        else:
            self.graph = graphx

    def to_string(self):
        return json.dumps(self.graph,indent=2)

    def get_system_node(self, system_node):
        if system_node not in self.graph[SYSTEM_NODES]:
            return None
        return self.graph[SYSTEM_NODES][system_node]

    def get_system_nodes(self):
        keys = list(self.graph[SYSTEM_NODES].keys())
        keys.sort()
        return keys

    def get_system_nodes_of_type(self, type):
        return [v for v in self.get_system_nodes() if self.is_system_node_of_type(v, type)]

    def has_system_node(self, system_node):
        return system_node in self.graph[SYSTEM_NODES]

    def get_relations(self):
        return self.graph[RELATIONS] if RELATIONS in self.graph else []

    @staticmethod
    def is_relation_of_type(edge, relation_type):
        if relation_type is None and "relation_type" not in edge:
            return True
        if "relation_type" in edge and edge["relation_type"] == relation_type:
            return True
        return False

    def get_relations_of_type(self, relation_type):
        return [e for e in self.get_relations() if system_model.is_relation_of_type(e, relation_type)]

    def is_system_node_of_type(self, system_node, type):
        return self.graph[SYSTEM_NODES][system_node]["type"] == type

    def add_system_node(self, key, type, **kwargs):
        if key in self.graph[SYSTEM_NODES]:
            return Response.error("System Node '{}' already exists".format(key))
        self.graph[SYSTEM_NODES][key] = kwargs
        self.graph[SYSTEM_NODES][key]["type"] = type
        return Response.success({key: self.get_system_node(key)})

    def add_relation(self, start, end, relation_type=None):
        if self.get_system_node(start) is None:
            return Response.error("Start node '{}' is not in the model".format(start))
        if self.get_system_node(end) is None:
            return Response.error("End node '{}' is not in the model".format(end))
        result = self.get_relation(start=start, end=end, relation_type=relation_type)
        if result.return_code == RESPONSE_OK:
            return Response.error("edge already exists")
        if result.content == "not found":
            result = {"start": start, "end": end}
            if relation_type is not None:
                result["relation_type"] = relation_type
            self.graph[RELATIONS].append(result)
            return Response.success()
        return Response.error(result.content)

    @staticmethod
    def get_related_system_node(system_node, edge):
        return edge["start"] if edge["end"] == system_node else edge["end"]

    def get_relations_of_system_node(self, with_system_node):
        return list(filter(lambda edge: with_system_node in (edge["start"], edge["end"]), self.get_relations()))

    def get_children(self, parent_system_node, of_type=None, in_relation_of=None):
        return list(
            filter(lambda child: of_type is None or self.is_system_node_of_type(child, of_type),
                   map(lambda edge: self.get_related_system_node(parent_system_node, edge),
                       filter(lambda edge: in_relation_of is None or system_model.is_relation_of_type(edge, in_relation_of),
                              self.get_relations_of_system_node(parent_system_node)))))

    def copy_system_node(self, from_model: 'system_model', system_node):
        vertex_value = dict(from_model.get_system_node(system_node))
        type = vertex_value.pop("type")
        self.add_system_node(system_node, type, **vertex_value)

    def _is_system_node_in_relations(self, system_node):
        for edge in self.get_relations():
            if self._is_relation_with_system_node(edge, system_node):
                return True
        return False

    def _is_relation_with_system_node(self, relation, system_node):
        return relation["start"] == system_node or relation["end"] == system_node

    def get_orphan_system_nodes(self, ofType):
        return [v for v in self.get_system_nodes_of_type(ofType) if not self._is_system_node_in_relations(v)]

    def set_model(self,new_model:'system_model'):
        self.graph = empty_graph()
        self.append(new_model)

    def append(self, to_append:'system_model'):
        for vertex in to_append.graph[SYSTEM_NODES]:
            self.graph[SYSTEM_NODES][vertex] = dict(to_append.graph[SYSTEM_NODES][vertex])
        for edge in to_append.graph[RELATIONS]:
            self.add_relation(edge["start"], edge["end"], edge["relation_type"] if "relation_type" in edge else None)

    def find_direct_connections(self, system_node, system_node_type=None, relation_type=None):
        connections = []
        for edge in self.get_relations_of_system_node(system_node):
            connection = self.get_related_system_node(system_node, edge)
            if relation_type is None or system_model.is_relation_of_type(edge, relation_type):
                if system_node_type is None or self.is_system_node_of_type(connection, system_node_type):
                    connections.append(connection)
        return connections

    def get_relation(self, start, end, relation_type):
        edges = list(
            filter(lambda edge: system_model.is_relation_of_type(edge, relation_type),
                   filter(lambda edge: start == edge["start"] and end == edge["end"], self.get_relations())))
        if edges is None or len(edges) == 0:
            return Response.error("not found")
        if len(edges) > 1:
            return Response.error("more then one edge ({}) found for (start={} end={} relation_type={})". \
                format(len(edges), start, end, relation_type))
        return Response.success(edges[0])

    def remove_relation(self, start, end, relation_type):
        result = self.get_relation(start, end, relation_type)
        if result.return_code == RESPONSE_ERROR:
            return result
        self.graph[RELATIONS].remove(result.content)
        return Response.success()


class component_model(system_model):
    def get_calling_relations(self):
        return self.get_relations_of_type("calls")

    def get_orphan_applications(self):
        return self.get_orphan_system_nodes("application")

    def is_product(self, system_node):
        return self.is_system_node_of_type(system_node, "product")

    def get_component_name(self, system_node):
        if "name" in self.graph[SYSTEM_NODES][system_node]:
            return self.graph[SYSTEM_NODES][system_node]["name"]
        return system_node

    def get_applications_in_product(self, product):
        return self.get_children(product, of_type="application", in_relation_of="contains")

    def getProducts(self):
        return self.get_system_nodes_of_type("product")


class data_model(system_model):
    def add_schema(self, schema):
        self.add_system_node(schema, "schema")

    def add_column(self, column, table):
        self.add_system_node(column, "column")
        self.add_relation(column, table)

    def add_table(self, table, schema):
        self.add_system_node(table, "table")
        self.add_relation(table, schema)

    def is_table(self, system_node):
        return self.is_system_node_of_type(system_node, "table")

    def get_table_for_column(self, column):
        column_edges = [edge for edge in self.get_relations_of_type(relation_type=RelationTypes.datamodel.contains)
                        if column in (edge["start"], edge["end"])]
        for edge in column_edges:
            system_node = self.get_related_system_node(column, edge)
            if self.is_table(system_node):
                return system_node
        return None

    def get_database_users(self):
        return self.get_system_nodes_of_type("database-user")

    def get_tables_in_database_user(self, database_user):
        return self.get_children(database_user, "table", "contains")

    def get_columns_in_table(self, table):
        return self.get_children(table, "column",in_relation_of=RelationTypes.datamodel.contains)

    def get_foreign_keys(self):
        return list(
            map(lambda fk: self._get_foreign_key(fk["start"], fk["end"]),
                self.get_relations_of_type("fk")))

    def _get_foreign_key(self, column1, column2):
        return {
            "start": {
                "column": column1,
                "table": self.get_table_for_column(column1)
            },
            "end": {
                "column": column2,
                "table": self.get_table_for_column(column2)
            }
        }

