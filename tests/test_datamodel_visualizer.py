import unittest


from smv import system_model_visualizer as svm
from smv.core.model.system_model import data_model, system_model as sm



class data_model_visualiser_test(unittest.TestCase):

    def test_draw_empty_database_user(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"}}
        }

        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","}","@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_draw_database_user_with_table(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"},
                        "TABLE1":{"type":"table"},
                        "TABLE2":{"type":"table"}},
            "edges":[{"start":"TABLE1","end":"SCHEMA1","relation_type":"contains"},
                     {"start":"TABLE2","end":"SCHEMA1","relation_type":"contains"}]
        }
        expected_result =["@startuml","left to right direction",
                          "package \"SCHEMA1\"{",
                          "class TABLE1 {","}",
                          "class TABLE2 {", "}",
                          "}",
                          "@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_start_database_user_end_table_relation(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"},
                        "TABLE1":{"type":"table"}},
            "edges":[{"end":"TABLE1","start":"SCHEMA1","relation_type":"contains"}]
        }
        expected_result =["@startuml","left to right direction",
                          "package \"SCHEMA1\"{",
                          "class TABLE1 {","}",
                          "}",
                          "@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_draw_table_with_column(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"},
                        "TABLE1":{"type":"table"},
                        "T1_ID":{"type":"column"}
        },
            "edges":[{"start":"TABLE1","end":"SCHEMA1","relation_type":"contains"},{"start":"T1_ID","end":"TABLE1"}]
        }
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","class TABLE1 {","+ T1_ID","}","}","@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result)

    def test_draw_table_with_colapsed_column(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"},
                        "TABLE1":{"type":"table"},
                        "T1_ID":{"type":"column"}
        },
            "edges":[{"start":"TABLE1","end":"SCHEMA1","relation_type":"contains"},{"start":"T1_ID","end":"TABLE1"}]
        }
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","class TABLE1 {","}","}","@enduml"]
        self.__run_draw_datamodel_test__(graph, expected_result, True)

    def test_draw_foreign_key(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"},"TABLE1":{"type":"table"},"TABLE2":{"type":"table"},
                        "T1_ID":{"type":"column"},"T2_ID":{"type":"column"}},
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1","relation_type":"contains"},
                {"start":"TABLE2","end":"SCHEMA1","relation_type":"contains"},
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
            "vertexes":{"SCHEMA1":{"type":"database-user"},"TABLE1":{"type":"table"},"TABLE2":{"type":"table"},
                        "T1_ID":{"type":"column"},"T2_ID":{"type":"column"}},
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1","relation_type":"contains"},
                {"start":"TABLE2","end":"SCHEMA1","relation_type":"contains"},
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

    def test_draw_database_user_uses_tables(self):
        # given
        model = data_model()
        model.add_vertex("user1","database-user")
        model.add_vertex("schema","database-user")
        model.add_vertex("table","table")
        model.add_vertex("c1","column")
        model.add_edge("user1","table","uses")
        model.add_edge("schema","table","contains")
        model.add_edge("c1","table","contains")

        # then
        expected = self.transform_in_lines("""
        @startuml
        left to right direction
        package "schema"{
        class table {
        + c1
        }
        }
        package "user1"{
        }
        @enduml
        """)

        self.__run_draw_datamodel_test__(model.graph, expected)

    def transform_in_lines(self, text:str):
        return list(
            filter(lambda line: False if line == '' else True,
            map(lambda line: line.lstrip(" "),text.split("\n"))))

    def test_draw_fk_over_two_database_user(self):
        graph = {
            "vertexes":{"SCHEMA1":{"type":"database-user"},
                        "SCHEMA2":{"type":"database-user"},
                        "TABLE1":{"type":"table"},
                        "TABLE2":{"type":"table"},
                        "T1_ID":{"type":"column"},
                        "T2_ID":{"type":"column"}},
            "edges":[
                {"start":"TABLE1","end":"SCHEMA1","relation_type":"contains"},
                {"start":"TABLE2","end":"SCHEMA2","relation_type":"contains"},
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

    def test_table_with_id(self):
        # given
        datamodel = data_model()
        datamodel.add_vertex("table_1", type="table",name="table 1")
        datamodel.add_vertex("schema1", type="database-user")
        datamodel.add_edge("schema1","table_1","contains")


        #then
        expected_result = ["@startuml",
                           "left to right direction",
                           "package \"schema1\"{",
                           "class \"table 1\" as table_1 {",
                           "}",
                           "}",
                           "@enduml"]

        self.__run_draw_datamodel_test__(datamodel.graph, expected_result)

    def __run_draw_datamodel_test__(self, graphDictionary, expectedResult, colapsed_columns = False):
        datamodel_graph = sm.data_model(graphDictionary)
        result = svm.datamodel_visualizer(datamodel_graph).draw(colapsed_columns)
        self.assertListEqual(expectedResult,result)

