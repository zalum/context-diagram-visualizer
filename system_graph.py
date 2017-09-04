import json

class Graph:

    def __init__(self,graphx = None):
        if graphx is None:
            self.graph = {"vertexes":{},"edges":[]}
        else:
            self.graph = graphx

    def to_json(self):
        return json.dumps(self.graph)
    def getVertexes(self):
        keys = list(self.graph["vertexes"].keys())
        keys.sort()
        return keys

    def getEdges(self):
        return self.graph["edges"] if "edges" in self.graph else []

    def is_vertex_of_type(self, vertex, type):
        return self.graph["vertexes"][vertex]["type"] == type

    def _isEdgeWithEndVertex(self,edge,vertex):
        return edge["end"] == vertex

    def does_vertex_exists(self,key):
        return key in self.graph["vertexes"]

    def add_vertex(self, key, type):
        if key in self.graph["vertexes"]:
            return
        self.graph["vertexes"][key] = {"type":type}

    def add_edge(self, startKey, endKey):
        edge = {"start":startKey,"end":endKey}
        self.graph["edges"].append(edge)

class SystemGraph(Graph):

    def edgeBetweenApplications(self,edge):
        for vertex in self.getVertexes():
            if self._isEdgeWithVertex(edge,vertex) and self.isProduct(vertex):
                return False
        return True

    def getOrphanApplications(self):
        edges = self.getEdges()
        return [vertex for vertex in self.getVertexes() if \
                self._isVertexInEdges(vertex,edges) is False \
                and self.isProduct(vertex) is False]

    def isProduct(self,vertex):
        return self.is_vertex_of_type(vertex, "product")

    def getVertexName(self,vertex):
        return self.graph["vertexes"][vertex]["name"]

    def getApplicationKeysInProduct(self,product):
        productEdges = list(filter(lambda edge: self._isEdgeWithEndVertex(edge,product),self.getEdges()))
        return list(map(lambda edge: self._getOppositeVertex(product,edge),productEdges))

    def _isVertexInEdges(self,vertex,edges):
        for edge in edges:
            if self._isEdgeWithVertex(edge,vertex):
                return True
        return False

    def _isEdgeWithVertex(self,edge,vertex):
        return edge["start"] == vertex or edge["end"] == vertex



    def _getOppositeVertex(self,vertex,edge):
        return  edge["start"] if edge["end"]==vertex else edge["end"]


class DatamodelGraph(Graph):
    def isSchema(self,vertex):
        return self.is_vertex_of_type(vertex, "schema")

    def add_schema(self,schema):
        self.add_vertex(schema,"schema")

    def add_column(self,column,table):
        self.add_vertex(column,"column")
        self.add_edge(column,table)

    def add_table(self,table,schema):
        self.add_vertex(table,"table")
        self.add_edge(table,schema)

    def _isTable(self, vertex):
        return self.is_vertex_of_type(vertex, "table")
    def _is_column(self,vertex):
        return self.is_vertex_of_type(vertex,"column")

    def get_table_for_column(self,column):
        column_edges = [edge for edge in self.getEdges() if edge["start"]==column]
        for edge in column_edges:
            vertex = edge["end"]
            if self._isTable(vertex):
                return vertex
        return None

    def getSchemas(self):
        return [vertex for vertex in self.getVertexes() if self.isSchema(vertex)]

    def get_tables_in_schema(self, schema):
        return [vertex for vertex in self.getVertexes() if self._isTableInSchema(vertex,schema)]

    def _isTableInSchema(self, vertex, schema):
        if self._isTable(vertex) is False:
            return False
        for edge in self.getEdges():
            if(edge["start"] == vertex and edge["end"] == schema):
                return True
        return False

    def get_columns_in_table(self, table):
        return list(filter(lambda v:self._is_column(v),
                map(lambda e: e["start"],
            filter(lambda edge: self._isEdgeWithEndVertex(edge,table),self.getEdges()))))

    def get_foreign_keys(self):
        return list(
            map(lambda fk: self._get_foreign_key(fk[0], fk[1]),
                filter(lambda e: self._is_column(e[0]) and self._is_column(e[1]),
                       map(lambda e: (e["start"],
                e["end"]), self.getEdges()))))

    def _get_foreign_key(self,column1, column2):
        return {
            "start":{
                "column":column1,
                "table":self.get_table_for_column(column1)
            },
            "end": {
                "column":column2,
                "table":self.get_table_for_column(column2)
            }
        }


