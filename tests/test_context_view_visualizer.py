import unittest
import system_graph
import graph_visualizer

class GraphVisualizerTestCases(unittest.TestCase):
  def testDrawOneRelation(self):
    graph = {
      "vertexes":[{"key":"1","name":"app1","type":"application"},{"key":"2","name":"app2","type":"application"}],
      "edges":[{"start":"1","end":"2"}]
      }
    expectedResult =["[app1]-->[app2]"]
    self.run_draw_context_diagram_test(graph,expectedResult)

  def testDrawProductWithOneApp(self):
      graph = {
        "vertexes":[{"key":"1","name":"app1","type":"product"},{"key":"2","name":"app2","type":"application"}],
        "edges":[{"start":"2","end":"1"}]
        }
      expectedResult =["folder app1{","[app2]","}"]
      self.run_draw_context_diagram_test(graph,expectedResult)

  def testDrawProudctWithOutgoingAppRelation(self):
      graph = {
        "vertexes":[{"key":"1","name":"app1","type":"application"},{"key":"2","name":"product","type":"product"}],
        "edges":[{"start":"2","end":"1"}]
        }
      expectedResult =["folder product{","}"]
      self.run_draw_context_diagram_test(graph,expectedResult)

  def testProductWithEdge(self):
       graph = {
         "vertexes":[{"key":"1","name":"app1","type":"application"},
                     {"key":"2","name":"product","type":"product"},
                     {"key":"3","name":"app2","type":"application"}],
         "edges":[{"start":"1","end":"2"},
                  {"start":"1","end":"3"}]
         }
       expectedResult =["folder product{","[app1]","}","[app1]-->[app2]"]
       self.run_draw_context_diagram_test(graph,expectedResult)

  def testNameEscaping(self):
      graph = {
          "vertexes":[{"key":"1","name":"app 1","type":"application"},
                      {"key":"2","name":"product 1","type":"product"},
                      {"key":"3","name":"app 2","type":"application"}],
          "edges":[{"start":"1","end":"2"},
                   {"start":"1","end":"3"}]
      }
      expectedResult =["folder product_1{","[app 1]","}","[app 1]-->[app 2]"]
      self.run_draw_context_diagram_test(graph,expectedResult)

  def run_draw_context_diagram_test(self, graphDictionary, expectedResult):
      systemGraph = system_graph.SystemGraph(graphDictionary)
      result = graph_visualizer.ContextDiagramGraphVisualizer(systemGraph).draw()
      self.assertListEqual(expectedResult,result)

