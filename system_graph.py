class SystemGraph:
    def __init__(self,graphDictionary):
        self.graph = graphDictionary

    def edgeBetweenApplications(self,edge):
        for vertex in self.getVertexes():
            if self._isEdgeWithVertex(edge,vertex) and self.isProduct(vertex):
                return False
        return True

    def getEdges(self):
        return self.graph["edges"]

    def getVertexes(self):
        return self.graph["vertexes"]

    def getOrphanApplications(self):
        edges = self.getEdges()
        return [vertex for vertex in self.getVertexes() if \
                self._isVertexInEdges(vertex,edges) is False \
                and self.isProduct(vertex) is False]

    def isProduct(self,vertex):
        return vertex["type"] == "product"

    def getVertexNameByKey(self,key):
        vertex = list(filter(lambda x: x["key"]==key,self.graph["vertexes"])).pop(0)
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

    def _isEdgeWithEndVertex(self,edge,vertex):
        return edge["end"] == vertex["key"]

    def _getOppositeVertex(self,vertex,edge):
        return  edge["start"] if edge["end"]==vertex["key"] else edge["end"]
