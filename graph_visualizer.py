class GraphVisualizer:
  def __init__(self,systemGraph):
      self.systemGraph = systemGraph

  def draw(self):
      orphanApplications = self.systemGraph.getOrphanApplications()
      lines = []
      [lines.extend(self._drawProduct(vertex)) for vertex in self.systemGraph.getVertexes() if self.systemGraph.isProduct(vertex)]
      lines.extend([self._drawEdges(edge) for edge in self.systemGraph.getEdges() if self.systemGraph.edgeBetweenApplications(edge)])
      lines.extend([self._drawApplication(vertex) for vertex in orphanApplications])
      return lines

  def _drawProduct(self,product):
      applicationsKey = self.systemGraph.getApplicationKeysInProduct(product)
      drawnProudct = ["folder %s{"%self.systemGraph.getVertexName(product)]
      drawnProudct.extend([self._drawApplicationByKey(applicationKey) for applicationKey in applicationsKey])
      drawnProudct.append("}")
      return drawnProudct
  def _drawApplicationByKey(self,key):
      return self._drawApplicationByName(self.systemGraph.getVertexNameByKey(key))
  def _drawApplicationByVertex(self,vertex):
      return self._drawApplicationByName(vertex["name"])
  def _drawApplicationByName(self,name):
    return "[%s]"%name
  def _drawEdges(self,edge):
      return "[%s]-->[%s]"%(self.systemGraph.getVertexNameByKey(edge["start"]),\
                            self.systemGraph.getVertexNameByKey(edge["end"]))
