import system_model

class ContextDiagramGraphVisualizer:
  def __init__(self,systemGraph):
      self.systemGraph = systemGraph

  def draw(self):
      orphanApplications = self.systemGraph.getOrphanApplications()
      lines = ["@startuml","left to right direction"]
      [lines.extend(self._drawProduct(vertex)) for vertex in self.systemGraph.getVertexes() if self.systemGraph.isProduct(vertex)]
      lines.extend([self._drawEdges(edge) for edge in self.systemGraph.getEdges() if self.systemGraph.edgeBetweenApplications(edge)])
      lines.extend([self._drawApplication(vertex) for vertex in orphanApplications])
      lines.append("@enduml")
      return lines

  def _drawProduct(self,product):
      applications = self.systemGraph.getApplicationKeysInProduct(product)
      drawnProudct = ["folder %s{"%self._drawProductName(product)]
      drawnProudct.extend([self._drawApplication(application) for application in applications])
      drawnProudct.append("}")
      return drawnProudct

  def _drawApplication(self, application):
      return self._drawApplicationByName(self.systemGraph.getVertexName(application))
  def _drawProductName(self,product):
      return self.systemGraph.getVertexName(product).replace(" ","_")
  def _drawApplicationByVertex(self,vertex):
      return self._drawApplicationByName(self.systemGraph.getVertexName(vertex))
  def _drawApplicationByName(self,name):
      return "[%s]"%name
  def _drawEdges(self,edge):
      return "[%s]-->[%s]"%(self.systemGraph.getVertexName(edge["start"]),\
                            self.systemGraph.getVertexName(edge["end"]))

class DatamodelVisualizer():
    def __init__(self,dataModelGraph):
        self.dataModelGraph = dataModelGraph

    def draw(self,colapsed_columns = False):
        lines = ["@startuml","left to right direction"]
        [lines.extend(self._drawSchema(schema,colapsed_columns)) for schema in self.dataModelGraph.getSchemas()]
        [lines.extend(self._draw_foreign_key(fk,colapsed_columns)) for fk in self.dataModelGraph.get_foreign_keys()]
        lines.append("@enduml")
        return lines


    def _drawSchema(self, schema,colapsed_columns = False):
        tables = self.dataModelGraph.get_tables_in_schema(schema)
        drawn_schema = ["package \"%s\"{"%schema]
        [drawn_schema.extend(self._draw_table(table,colapsed_columns)) for table in tables]
        drawn_schema.append("}")
        return drawn_schema

    def _draw_table(self, table,colapsed_columns=False):
        drawn_table = ["class %s {"%table]
        columns = self.dataModelGraph.get_columns_in_table(table)
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

