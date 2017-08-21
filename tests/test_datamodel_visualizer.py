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

    def test_draw_table_with_column(self):
        graph = {
            "vertexes":[{"key":"SCHEMA1","type":"schema"},
                        {"key":"TABLE1","type":"table"},
                        {"key":"T1_ID","type":"column"}
                        ],
            "edges":[{"start":"TABLE1","end":"SCHEMA1"},{"start":"T1_ID","end":"TABLE1"}]
        }
        expected_result =["package \"SCHEMA1\"{","class TABLE1 {","+ T1_ID","}","}"]
        self.run_draw_datamodel_test(graph,expected_result)

    def test_draw_table_with_colapsed_column(self):
        graph = {
            "vertexes":[{"key":"SCHEMA1","type":"schema"},
                        {"key":"TABLE1","type":"table"},
                        {"key":"T1_ID","type":"column"}
                        ],
            "edges":[{"start":"TABLE1","end":"SCHEMA1"},{"start":"T1_ID","end":"TABLE1"}]
        }
        expected_result =["package \"SCHEMA1\"{","class TABLE1 {","}","}"]
        self.run_draw_datamodel_test(graph,expected_result,True)



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
        expected_result = ["package \"SCHEMA1\"{",
                         "class TABLE1 {",
                         "+ T1_ID",
                         "}",
                         "class TABLE2 {",
                         "+ T2_ID",
                         "}",
                         "}",
                         "TABLE1::T1_ID --> TABLE2::T2_ID"
                         ]

        self.run_draw_datamodel_test(graph,expected_result)

    def test_draw_table_with_colapsed_column_with_fk(self):
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
        expected_result = ["package \"SCHEMA1\"{",
                           "class TABLE1 {",
                           "}",
                           "class TABLE2 {",
                           "}",
                           "}",
                           "TABLE1 --> TABLE2 : T1_ID::T2_ID"
                           ]

        self.run_draw_datamodel_test(graph,expected_result,colapsed_columns=True)


    def test_draw_fk_over_two_schemas(self):
        graph = {
            "vertexes":[{"key":"SCHEMA1","type":"schema"},
                        {"key":"SCHEMA2","type":"schema"},
                        {"key":"TABLE1","type":"table"},
                        {"key":"TABLE2","type":"table"},
                        {"key":"T1_ID","type":"column"},
                        {"key":"T2_ID","type":"column"}],
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1"},
                {"start":"TABLE2","end":"SCHEMA2"},
                {"start":"T1_ID","end":"TABLE1"},
                {"start":"T2_ID","end":"TABLE2"},
                {"start":"T1_ID","end":"T2_ID"},
            ]
        }

        expected_result = ["package \"SCHEMA1\"{",
                          "class TABLE1 {",
                          "+ T1_ID",
                          "}",
                          "}",
                          "package \"SCHEMA2\"{",
                          "class TABLE2 {",
                          "+ T2_ID",
                          "}",
                          "}",
                          "TABLE1::T1_ID --> TABLE2::T2_ID"
                          ]
        self.run_draw_datamodel_test(graph,expected_result)

    def run_draw_datamodel_test(self, graphDictionary, expectedResult,colapsed_columns = False):
        datamodel_graph = system_graph.DatamodelGraph(graphDictionary)
        result = graph_visualizer.DatamodelVisualizer(datamodel_graph).draw(colapsed_columns)
        self.assertListEqual(expectedResult,result)

