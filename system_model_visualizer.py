import system_model as sm
class component_model_visualizer:

  def __init__(self, system_model: sm.component_model):
      self.system_model = system_model

  def draw(self):
      orphanApplications = self.system_model.getOrphanApplications()
      lines = ["@startuml","left to right direction"]
      [lines.extend(self._drawProduct(vertex)) for vertex in self.system_model.getProducts()]
      lines.extend([self._drawEdges(edge) for edge in self.system_model.getEdges() if self.system_model.edgeBetweenApplications(edge)])
      lines.extend([self._drawApplication(vertex) for vertex in orphanApplications])
      lines.append("@enduml")
      return lines

  def _drawProduct(self,product):
      applications = self.system_model.getApplicationsInProduct(product)
      drawnProudct = ["folder %s{"%self._drawProductName(product)]
      drawnProudct.extend([self._drawApplication(application) for application in applications])
      drawnProudct.append("}")
      return drawnProudct

  def _drawApplication(self, application):
      return self._drawApplicationByName(self.system_model.getVertexName(application))
  def _drawProductName(self,product):
      return self.system_model.getVertexName(product).replace(" ", "_")
  def _drawApplicationByVertex(self,vertex):
      return self._drawApplicationByName(self.system_model.getVertexName(vertex))
  def _drawApplicationByName(self,name):
      return "[%s]"%name
  def _drawEdges(self,edge):
      return "[%s]-->[%s]"%(self.system_model.getVertexName(edge["start"]),\
                            self.system_model.getVertexName(edge["end"]))

class datamodel_visualizer():
    def __init__(self, system_model: sm.data_model):
        self.system_model = system_model

    def draw(self,colapsed_columns = False):
        lines = ["@startuml","left to right direction"]
        [lines.extend(self._drawSchema(schema,colapsed_columns)) for schema in self.system_model.getSchemas()]
        [lines.extend(self._draw_foreign_key(fk,colapsed_columns)) for fk in self.system_model.get_foreign_keys()]
        lines.append("@enduml")
        return lines


    def _drawSchema(self, schema,colapsed_columns = False):
        tables = self.system_model.get_tables_in_schema(schema)
        drawn_schema = ["package \"%s\"{"%schema]
        [drawn_schema.extend(self._draw_table(table,colapsed_columns)) for table in tables]
        drawn_schema.append("}")
        return drawn_schema

    def _draw_table(self, table,colapsed_columns=False):
        drawn_table = ["class %s {"%table]
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

