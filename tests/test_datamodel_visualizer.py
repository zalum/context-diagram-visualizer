import unittest
import graph_visualizer
import system_graph


class DatamodelVisualizerTestCases(unittest.TestCase):

    def test_draw_empty_schema(self):
        graph = {
            "vertexes":[{"key":"SCHEMA1","type":"schema"}]
        }

        expected_result =["package \"SCHEMA1\"{","}"]
        self.run_draw_datamodel_test(graph,expected_result)

    def test_draw_schema_with_table(self):
        graph = {
            "vertexes":[{"key":"SCHEMA1","type":"schema"},{"key":"TABLE1","type":"table"}],
            "edges":[{"start":"TABLE1","end":"SCHEMA1"}]
        }
        expected_result =["package \"SCHEMA1\"{","class TABLE1 {","}","}"]
        self.run_draw_datamodel_test(graph,expected_result)

    def test_draw_foreign_key(self):
        graph = {
            "vertexes":[{"key":"SCHEMA1","type":"schema"},{"key":"TABLE1","type":"table"},{"key":"TABLE2","type":"table"},
                        {"key":"T1_ID","type":"column"},{"key":"T2_ID","type":"column"}],
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1"},
                {"start":"TABLE2","end":"SCHEMA1"},
                {"start":"T1_ID","end":"TABLE1"},
                {"start":"T2_ID","end":"TABLE2"},
                {"start":"T1_ID","end":"T2_ID"},
            ]
        }
        expected_result =["package \"SCHEMA1\"{",
                         "class TABLE1 {",
                         "+ T1_ID",
                         "}",
                         "class TABLE2 {",
                         "+ T2_ID",
                         "}",
                         "TABLE1::T1_ID --> TABLE2::T2_ID","}"
                         ]

        self.run_draw_datamodel_test(graph,expected_result)



    def run_draw_datamodel_test(self, graphDictionary, expectedResult):
        datamodel_graph = system_graph.DatamodelGraph(graphDictionary)
        result = graph_visualizer.DatamodelVisualizer(datamodel_graph).draw()
        self.assertListEqual(expectedResult,result)

