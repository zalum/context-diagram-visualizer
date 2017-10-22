import unittest
import system_model as sm
import system_model_visualizer as svm

class component_model_visualizer_test(unittest.TestCase):
  def testDrawOneRelation(self):
    graph = {
      "vertexes":{"1":{"name":"app1","type":"application"},"2":{"name":"app2","type":"application"}},
      "edges":[{"start":"1","end":"2"}]
      }
    expectedResult =["@startuml","left to right direction","[app1]-->[app2]","@enduml"]
    self.__run_draw_context_diagram_test__(graph, expectedResult)

  def testDrawProductWithOneApp(self):
      graph = {
        "vertexes":{"1":{"name":"app1","type":"product"},"2":{"name":"app2","type":"application"}},
        "edges":[{"start":"2","end":"1"}]
        }
      expectedResult =["@startuml","left to right direction","folder app1{","[app2]","}","@enduml"]
      self.__run_draw_context_diagram_test__(graph, expectedResult)

  def testDrawProductWithOneAppStartUnidirectionalRelation(self):
      graph = {
        "vertexes":{"1":{"name":"app1","type":"application"},"2":{"name":"product","type":"product"}},
        "edges":[{"start":"2","end":"1"}]
        }
      expectedResult =["@startuml","left to right direction","folder product{","[app1]","}","@enduml"]
      self.__run_draw_context_diagram_test__(graph, expectedResult)

  def testProductWithEdge(self):
       graph = {
         "vertexes":{"1":{"name":"app1","type":"application"},
                     "2":{"name":"product","type":"product"},
                     "3":{"name":"app2","type":"application"}},
         "edges":[{"start":"1","end":"2"},
                  {"start":"1","end":"3"}]
         }
       expectedResult =["@startuml","left to right direction","folder product{","[app1]","}","[app1]-->[app2]","@enduml"]
       self.__run_draw_context_diagram_test__(graph, expectedResult)

  def testNameEscaping(self):
      graph = {
          "vertexes":{"1":{"name":"app 1","type":"application"},
                      "2":{"name":"product 1","type":"product"},
                      "3":{"name":"app 2","type":"application"}},
          "edges":[{"start":"1","end":"2"},
                   {"start":"1","end":"3"}]
      }
      expectedResult =["@startuml","left to right direction","folder product_1{","[app 1]","}","[app 1]-->[app 2]","@enduml"]
      self.__run_draw_context_diagram_test__(graph, expectedResult)

  def __run_draw_context_diagram_test__(self, graphDictionary, expectedResult):
      systemGraph = sm.component_model(graphDictionary)
      result = svm.component_model_visualizer(systemGraph).draw()
      self.assertListEqual(expectedResult,result)

