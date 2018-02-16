import json
from smv.core import Response

def empty_graph():
    return {"vertexes": {}, "edges": []}

RESPONSE_OK = object()


class system_model:
    def __init__(self, graphx=None):
        if graphx is None or len(graphx.keys()) == 0:
            self.graph = empty_graph()
        else:
            self.graph = graphx

    def to_string(self):
        return json.dumps(self.graph,indent=2)

    def get_vertex(self, vertex):
        if vertex not in self.graph["vertexes"]:
            return None
        return self.graph["vertexes"][vertex]

    def getVertexes(self):
        keys = list(self.graph["vertexes"].keys())
        keys.sort()
        return keys

    def has_vertex(self, vertex):
        return vertex in self.graph["vertexes"]

    def get_edges(self):
        return self.graph["edges"] if "edges" in self.graph else []

    @staticmethod
    def is_edge_of_type(edge, relation_type):
        if relation_type is None and "relation_type" not in edge:
            return True
        if "relation_type" in edge and edge["relation_type"] == relation_type:
            return True
        return False

    def get_edges_of_type(self, relation_type):
        return [e for e in self.get_edges() if system_model.is_edge_of_type(e, relation_type)]

    def is_vertex_of_type(self, vertex, type):
        return self.graph["vertexes"][vertex]["type"] == type

    def does_vertex_exists(self, key):
        return key in self.graph["vertexes"]

    def add_vertex(self, key, type, **kwargs):
        if key in self.graph["vertexes"]:
            return Response.error("System Node '{}' already exists".format(key))
        self.graph["vertexes"][key] = kwargs
        self.graph["vertexes"][key]["type"] = type
        return Response.success({key: self.get_vertex(key)})

    def add_edge(self, start, end, relation_type=None):
        if self.get_vertex(start) is None:
            return "Start node is not in the model"
        if self.get_vertex(end) is None:
            return "End node is not in the model"
        result = self.get_edge(start=start, end=end, relation_type=relation_type)
        if result is None:
            result = {"start": start, "end": end}
            if relation_type is not None:
                result["relation_type"] = relation_type
            self.graph["edges"].append(result)
        else:
            if type(result) != dict:
                return result
        return RESPONSE_OK

    def get_related_vertex(self, vertex, edge):
        return edge["start"] if edge["end"] == vertex else edge["end"]

    def get_edges_of_vertex(self, with_vertex):
        return list(filter(lambda edge: with_vertex in (edge["start"], edge["end"]), self.get_edges()))

    def get_children(self, parent_vertex, of_type=None, in_relation_of=None):
        return list(
            filter(lambda child: of_type is None or self.is_vertex_of_type(child, of_type),
                   map(lambda edge: self.get_related_vertex(parent_vertex, edge),
                       filter(lambda edge: in_relation_of is None or system_model.is_edge_of_type(edge, in_relation_of),
                              self.get_edges_of_vertex(parent_vertex)))))

    def get_vertexes_of_type(self, type):
        return [v for v in self.getVertexes() if self.is_vertex_of_type(v, type)]

    def copy_vertex(self,from_model: 'system_model', vertex):
        vertex_value = dict(from_model.get_vertex(vertex))
        type = vertex_value.pop("type")
        self.add_vertex(vertex, type, **vertex_value)


    def _is_vertex_in_edges(self, vertex):
        for edge in self.get_edges():
            if self._is_edge_with_vertex(edge, vertex):
                return True
        return False

    def _is_edge_with_vertex(self, edge, vertex):
        return edge["start"] == vertex or edge["end"] == vertex

    def get_orphan_vertexes(self, ofType):
        return [v for v in self.get_vertexes_of_type(ofType) if not self._is_vertex_in_edges(v)]

    def set_model(self,new_model:'system_model'):
        self.graph = empty_graph()
        self.append(new_model)

    def append(self, to_append:'system_model'):
        for vertex in to_append.graph["vertexes"]:
            self.graph["vertexes"][vertex] = dict(to_append.graph["vertexes"][vertex])
        for edge in to_append.graph["edges"]:
            self.add_edge(edge["start"], edge["end"], edge["relation_type"] if "relation_type" in edge else None)

    def find_direct_connections(self, vertex, vertex_type=None, relation_type=None):
        connections = []
        for edge in self.get_edges_of_vertex(vertex):
            connection = self.get_related_vertex(vertex, edge)
            if relation_type is None or system_model.is_edge_of_type(edge, relation_type):
                if vertex_type is None or self.is_vertex_of_type(connection, vertex_type):
                    connections.append(connection)
        return connections

    def get_edge(self, start, end, relation_type):
        edges = list(
            filter(lambda edge: system_model.is_edge_of_type(edge, relation_type),
                   filter(lambda edge: start == edge["start"] and end == edge["end"], self.get_edges())))
        if edges is None or len(edges) == 0:
            return None
        if len(edges) > 1:
            return "more then one edge ({}) found for (start={} end={} relation_type={})". \
                format(len(edges), start, end, relation_type)
        return edges[0]


class component_model(system_model):
    def get_calling_relations(self):
        return self.get_edges_of_type("calls")

    def get_orphan_applications(self):
        return self.get_orphan_vertexes("application")

    def isProduct(self, vertex):
        return self.is_vertex_of_type(vertex, "product")

    def getVertexName(self, vertex):
        if "name" in self.graph["vertexes"][vertex]:
            return self.graph["vertexes"][vertex]["name"]
        return vertex

    def getApplicationsInProduct(self, product):
        return self.get_children(product, of_type="application", in_relation_of="contains")

    def getProducts(self):
        return self.get_vertexes_of_type("product")


class data_model(system_model):
    def add_schema(self, schema):
        self.add_vertex(schema, "schema")

    def add_column(self, column, table):
        self.add_vertex(column, "column")
        self.add_edge(column, table)

    def add_table(self, table, schema):
        self.add_vertex(table, "table")
        self.add_edge(table, schema)

    def _isTable(self, vertex):
        return self.is_vertex_of_type(vertex, "table")

    def get_table_for_column(self, column):
        column_edges = [edge for edge in self.get_edges() if edge["start"] == column]
        for edge in column_edges:
            vertex = edge["end"]
            if self._isTable(vertex):
                return vertex
        return None

    def getSchemas(self):
        return self.get_vertexes_of_type("schema")

    def get_database_users(self):
        return self.get_vertexes_of_type("database-user")

    def get_tables_in_database_user(self, database_user):
        return self.get_children(database_user, "table", "contains")

    def get_columns_in_table(self, table):
        return self.get_children(table, "column")

    def get_foreign_keys(self):
        return list(
            map(lambda fk: self._get_foreign_key(fk["start"], fk["end"]),
                self.get_edges_of_type("fk")))

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
