
class Graph:
    def __init__(self,graph):
        self.graph = graph
    def getVertexes(self):
        return self.graph["vertexes"]

    def getEdges(self):
        return self.graph["edges"]

    def is_vertex_of_type(self, vertex, type):
        return vertex["type"] == type

    def _isEdgeWithEndVertex(self,edge,vertex):
        return edge["end"] == vertex["key"]

    def _get_vertex_by_key(self, key):
        return list(filter(lambda x: x["key"]==key,self.getVertexes())).pop(0)

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

    def getVertexNameByKey(self,key):
        vertex = self._get_vertex_by_key(key)
        return self.getVertexName(vertex)

    def getVertexName(self,vertex):
        return vertex["name"]

    def getApplicationKeysInProduct(self,product):
        productEdges = list(filter(lambda edge: self._isEdgeWithEndVertex(edge,product),self.getEdges()))
        return list(map(lambda edge: self._getOppositeVertex(product,edge),productEdges))

    def _isVertexInEdges(self,vertex,edges):
        for edge in edges:
            if self._isEdgeWithVertex(edge,vertex):
                return True
        return False

    def _isEdgeWithVertex(self,edge,vertex):
        return edge["start"] == vertex["key"] or edge["end"] == vertex["key"]



    def _getOppositeVertex(self,vertex,edge):
        return  edge["start"] if edge["end"]==vertex["key"] else edge["end"]




class DatamodelGraph(Graph):
    def isSchema(self,vertex):
        return self.is_vertex_of_type(vertex, "schema")

    def _isTable(self, vertex):
        return self.is_vertex_of_type(vertex, "table")
    def _is_column(self,vertex):
        return self.is_vertex_of_type(vertex,"column")

    def get_table_for_column(self,column):
        column_edges = [edge for edge in self.getEdges() if edge["start"]==column["key"]]
        for edge in column_edges:
            vertex = self._get_vertex_by_key(edge["end"])
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
            if(edge["start"] == vertex["key"] and edge["end"] == schema["key"]):
                return True
        return False

    def get_columns_in_table(self, table):
        return list(filter(lambda v:self._is_column(v),
            map(lambda key: self._get_vertex_by_key(key),
            map(lambda e: e["start"],
            filter(lambda edge: self._isEdgeWithEndVertex(edge,table),self.getEdges())))))

    def get_foreign_keys(self):
        return list(
            map(lambda fk: self._get_foreign_key(fk[0], fk[1]),
            filter(lambda e: self._is_column(e[0]) and self._is_column(e[1]),
            map(lambda e: (self._get_vertex_by_key(e["start"]),
                self._get_vertex_by_key(e["end"])),self.getEdges()))))

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
