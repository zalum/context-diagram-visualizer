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
    self._runDrawTest(graph,expectedResult)

  def testDrawProductWithOneApp(self):
      graph = {
        "vertexes":[{"key":"1","name":"app1","type":"product"},{"key":"2","name":"app2","type":"application"}],
        "edges":[{"start":"2","end":"1"}]
        }
      expectedResult =["folder app1{","[app2]","}"]
      self._runDrawTest(graph,expectedResult)
  def testDrawProudctWithOutgoingAppRelation(self):
      graph = {
        "vertexes":[{"key":"1","name":"app1","type":"application"},{"key":"2","name":"product","type":"product"}],
        "edges":[{"start":"2","end":"1"}]
        }
      expectedResult =["folder product{","}"]
      self._runDrawTest(graph,expectedResult)
  def testProductWithEdge(self):
       graph = {
         "vertexes":[{"key":"1","name":"app1","type":"application"},
                     {"key":"2","name":"product","type":"product"},
                     {"key":"3","name":"app2","type":"application"}],
         "edges":[{"start":"1","end":"2"},
                  {"start":"1","end":"3"}]
         }
       expectedResult =["folder product{","[app1]","}","[app1]-->[app2]"]
       self._runDrawTest(graph,expectedResult)
  def _runDrawTest(self, graphDictionary,expectedResult):
     systemGraph = system_graph.SystemGraph(graphDictionary)
     result = graph_visualizer.GraphVisualizer(systemGraph).draw()
     self.assertListEqual(expectedResult,result)
