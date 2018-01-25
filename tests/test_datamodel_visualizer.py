import unittest

from smv import system_model_visualizer as svm
from smv.core.model import system_model as sm


class data_model_visualiser_test(unittest.TestCase):

    def test_draw_empty_schema(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"}}
        }

        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","}","@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_draw_schema_with_table(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},
                        "TABLE1":{"type":"table"},
                        "TABLE2":{"type":"table"}},
            "edges":[{"start":"TABLE1","end":"SCHEMA1"},
                     {"start":"TABLE2","end":"SCHEMA1"}]
        }
        expected_result =["@startuml","left to right direction",
                          "package \"SCHEMA1\"{",
                          "class TABLE1 {","}",
                          "class TABLE2 {", "}",
                          "}",
                          "@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_start_schema_end_table_relation(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},
                        "TABLE1":{"type":"table"}},
            "edges":[{"end":"TABLE1","start":"SCHEMA1"}]
        }
        expected_result =["@startuml","left to right direction",
                          "package \"SCHEMA1\"{",
                          "class TABLE1 {","}",
                          "}",
                          "@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_draw_table_with_column(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},
                        "TABLE1":{"type":"table"},
                        "T1_ID":{"type":"column"}
        },
            "edges":[{"start":"TABLE1","end":"SCHEMA1"},{"start":"T1_ID","end":"TABLE1"}]
        }
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","class TABLE1 {","+ T1_ID","}","}","@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)


    def test_draw_table_with_colapsed_column(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},
                        "TABLE1":{"type":"table"},
                        "T1_ID":{"type":"column"}
        },
            "edges":[{"start":"TABLE1","end":"SCHEMA1"},{"start":"T1_ID","end":"TABLE1"}]
        }
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","class TABLE1 {","}","}","@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result, True)



    def test_draw_foreign_key(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},"TABLE1":{"type":"table"},"TABLE2":{"type":"table"},
                        "T1_ID":{"type":"column"},"T2_ID":{"type":"column"}},
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1"},
                {"start":"TABLE2","end":"SCHEMA1"},
                {"start":"T1_ID","end":"TABLE1"},
                {"start":"T2_ID","end":"TABLE2"},
                {"start":"T1_ID","end":"T2_ID","relation_type":"fk"},
            ]
        }
        expected_result = ["@startuml","left to right direction","package \"SCHEMA1\"{",
                         "class TABLE1 {",
                         "+ T1_ID",
                         "}",
                         "class TABLE2 {",
                         "+ T2_ID",
                         "}",
                         "}",
                         "TABLE1::T1_ID --> TABLE2::T2_ID","@enduml"
                         ]

        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_draw_table_with_colapsed_column_with_fk(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},"TABLE1":{"type":"table"},"TABLE2":{"type":"table"},
                        "T1_ID":{"type":"column"},"T2_ID":{"type":"column"}},
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1"},
                {"start":"TABLE2","end":"SCHEMA1"},
                {"start":"T1_ID","end":"TABLE1"},
                {"start":"T2_ID","end":"TABLE2"},
                {"start":"T1_ID","end":"T2_ID","relation_type":"fk"},
            ]
        }
        expected_result = ["@startuml","left to right direction","package \"SCHEMA1\"{",
                           "class TABLE1 {",
                           "}",
                           "class TABLE2 {",
                           "}",
                           "}",
                           "TABLE1 --> TABLE2 : T1_ID::T2_ID","@enduml"
                           ]

        self.__run_draw_datamodel_test__(graph, expected_result, colapsed_columns=True)


    def test_draw_fk_over_two_schemas(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"schema"},
                        "SCHEMA2":{"type":"schema"},
                        "TABLE1":{"type":"table"},
                        "TABLE2":{"type":"table"},
                        "T1_ID":{"type":"column"},
                        "T2_ID":{"type":"column"}},
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1"},
                {"start":"TABLE2","end":"SCHEMA2"},
                {"start":"T1_ID","end":"TABLE1"},
                {"start":"T2_ID","end":"TABLE2"},
                {"start":"T1_ID","end":"T2_ID","relation_type":"fk"},
            ]
        }

        expected_result = ["@startuml","left to right direction","package \"SCHEMA1\"{",
                          "class TABLE1 {",
                          "+ T1_ID",
                          "}",
                          "}",
                          "package \"SCHEMA2\"{",
                          "class TABLE2 {",
                          "+ T2_ID",
                          "}",
                          "}",
                          "TABLE1::T1_ID --> TABLE2::T2_ID","@enduml"
                          ]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_constructor_when_default_parameter_is_mutated(self):
        """
        http://docs.python-guide.org/en/latest/writing/gotchas/
        """

        datamodel_graph = sm.data_model()
        datamodel_graph.add_schema("SCHEMA1")

        result = svm.datamodel_visualizer(datamodel_graph).draw()
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","}","@enduml"]
        self.assertListEqual(expected_result,result)

        datamodel_graph = sm.data_model()
        result = svm.datamodel_visualizer(datamodel_graph).draw()
        self.assertListEqual(["@startuml","left to right direction","@enduml"],result)


    def __run_draw_datamodel_test__(self, graphDictionary, expectedResult, colapsed_columns = False):
        datamodel_graph = sm.data_model(graphDictionary)
        result = svm.datamodel_visualizer(datamodel_graph).draw(colapsed_columns)
        self.assertListEqual(expectedResult,result)

