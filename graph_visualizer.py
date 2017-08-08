import system_graph

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
      drawnProudct = ["folder %s{"%self._drawProductName(product)]
      drawnProudct.extend([self._drawApplicationByKey(applicationKey) for applicationKey in applicationsKey])
      drawnProudct.append("}")
      return drawnProudct

  def _drawApplicationByKey(self,key):
      return self._drawApplicationByName(self.systemGraph.getVertexNameByKey(key))
  def _drawProductName(self,product):
      return self.systemGraph.getVertexName(product).replace(" ","_")
  def _drawApplicationByVertex(self,vertex):
      return self._drawApplicationByName(self.systemGraph.getVertexName(vertex))
  def _drawApplicationByName(self,name):
      return "[%s]"%name
  def _drawEdges(self,edge):
      return "[%s]-->[%s]"%(self.systemGraph.getVertexNameByKey(edge["start"]),\
                            self.systemGraph.getVertexNameByKey(edge["end"]))

class DatamodelVisualizer():
    def __init__(self,dataModelGraph):
        """
        :type dataModelGraph: system_graph.DatamodelGraph
        """
        self.dataModelGraph = dataModelGraph

    def draw(self):
        lines = []
        [lines.extend(self._drawSchema(schema)) for schema in self.dataModelGraph.getSchemas()]
        return lines


    def _drawSchema(self, schema):
        tables = self.dataModelGraph.get_tables_in_schema(schema)
        foreign_keys = self.dataModelGraph.get_foreign_keys()
        drawn_schema = ["package \"%s\"{"%schema["key"]]
        [drawn_schema.extend(self._draw_table(table)) for table in tables]
        [drawn_schema.extend(self._draw_foreign_key(fk)) for fk in foreign_keys]

        drawn_schema.append("}")
        return drawn_schema

    def _draw_table(self, table):
        drawn_table = ["class %s {"%table["key"]]
        columns = self.dataModelGraph.get_columns_in_table(table)
        [drawn_table.extend(self._draw_column(column)) for column in columns]
        drawn_table.extend("}")
        return drawn_table

    def _draw_column(self, column):
        return ["+ %s"%column["key"]]

    def _draw_foreign_key(self, fk):
        return ["%s::%s --> %s::%s"% \
        (fk["start"]["table"]["key"],
         fk["start"]["column"]["key"],
         fk["end"]["table"]["key"],
         fk["end"]["column"]["key"])]

