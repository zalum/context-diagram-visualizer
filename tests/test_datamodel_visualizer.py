import unittest


from smv import system_model_visualizer as svm
import smv.core.model.system_model as sm



class DataModelVisualiserTest(unittest.TestCase):

    def test_draw_empty_database_user(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1",type="database-user")

        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","}","@enduml"]
        self.__run_draw_datamodel_test__(model, expected_result)

    def test_draw_database_user_with_table(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1",type="database-user")
        model.add_system_node("TABLE1",type="table")
        model.add_system_node("TABLE2",type="table")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="TABLE2", end="SCHEMA1", relation_type="contains")
        
        expected_result =["@startuml","left to right direction",
                          "package \"SCHEMA1\"{",
                          "class TABLE1 {","}",
                          "class TABLE2 {", "}",
                          "}",
                          "@enduml"]
        self.__run_draw_datamodel_test__(model, expected_result)

    def test_start_database_user_end_table_relation(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1",type="database-user")
        model.add_system_node("TABLE1",type="table")
        model.add_relation("SCHEMA1", "TABLE1", "contains")
        expected_result =["@startuml","left to right direction",
                          "package \"SCHEMA1\"{",
                          "class TABLE1 {","}",
                          "}",
                          "@enduml"]
        self.__run_draw_datamodel_test__(model, expected_result)

    def test_draw_table_with_column(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1",type="database-user")
        model.add_system_node("TABLE1",type="table")
        model.add_system_node("T1_ID",type="column")       
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="T1_ID", end="TABLE1")
        
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","class TABLE1 {","+ T1_ID","}","}","@enduml"]
        self.__run_draw_datamodel_test__(model, expected_result)

    def test_draw_table_with_colapsed_column(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1",type="database-user")
        model.add_system_node("TABLE1",type="table")
        model.add_system_node("T1_ID",type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="T1_ID", end="TABLE1")
        expected_result =["@startuml","left to right direction","package \"SCHEMA1\"{","class TABLE1 {","}","}","@enduml"]
        self.__run_draw_datamodel_test__(model, expected_result, True)

    def test_draw_foreign_key(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type="database-user")
        model.add_system_node("TABLE1", type="table")
        model.add_system_node("TABLE2", type="table")
        model.add_system_node("T1_ID", type="column")
        model.add_system_node("T2_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="TABLE2", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="T1_ID", end="TABLE1")
        model.add_relation(start="T2_ID", end="TABLE2")
        model.add_relation(start="T1_ID", end="T2_ID", relation_type="fk")

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

        self.__run_draw_datamodel_test__(model, expected_result)

    def test_draw_table_with_colapsed_column_with_fk(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type = "database-user")
        model.add_system_node("TABLE1", type = "table")
        model.add_system_node("TABLE2", type="table")
        model.add_system_node("T1_ID", type="column")
        model.add_system_node("T2_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="TABLE2", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="T1_ID", end="TABLE1")
        model.add_relation(start="T2_ID", end="TABLE2")
        model.add_relation(start="T1_ID", end="T2_ID", relation_type="fk")

        expected_result = ["@startuml","left to right direction","package \"SCHEMA1\"{",
                           "class TABLE1 {",
                           "}",
                           "class TABLE2 {",
                           "}",
                           "}",
                           "TABLE1 --> TABLE2 : T1_ID::T2_ID","@enduml"
                           ]

        self.__run_draw_datamodel_test__(model, expected_result, colapsed_columns=True)

    def test_draw_database_user_uses_tables(self):
        # given
        model = sm.data_model()
        model.add_system_node("user1", "database-user")
        model.add_system_node("schema", "database-user")
        model.add_system_node("table", "table")
        model.add_system_node("c1", "column")
        model.add_relation("user1", "table", "uses")
        model.add_relation("schema", "table", "contains")
        model.add_relation("c1", "table", "contains")

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

        self.__run_draw_datamodel_test__(model, expected)

    def transform_in_lines(self, text:str):
        return list(
            filter(lambda line: False if line == '' else True,
            map(lambda line: line.lstrip(" "),text.split("\n"))))

    def test_draw_fk_over_two_database_user(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1",type="database-user")
        model.add_system_node("SCHEMA2",type="database-user")
        model.add_system_node("TABLE1",type="table")
        model.add_system_node("TABLE2",type="table")
        model.add_system_node("T1_ID",type="column")
        model.add_system_node("T2_ID",type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type="contains")
        model.add_relation(start="TABLE2", end="SCHEMA2", relation_type="contains")
        model.add_relation(start="T1_ID", end="TABLE1")
        model.add_relation(start="T2_ID", end="TABLE2")
        model.add_relation(start="T1_ID", end="T2_ID", relation_type="fk")

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
        self.__run_draw_datamodel_test__(model, expected_result)

    def test_table_with_id(self):
        # given
        datamodel = sm.data_model()
        datamodel.add_system_node("table_1", type="table", name="table 1")
        datamodel.add_system_node("schema1", type="database-user")
        datamodel.add_relation("schema1", "table_1", "contains")


        # then
        expected_result = ["@startuml",
                           "left to right direction",
                           "package \"schema1\"{",
                           "class \"table 1\" as table_1 {",
                           "}",
                           "}",
                           "@enduml"]

        self.__run_draw_datamodel_test__(datamodel, expected_result)

    def __run_draw_datamodel_test__(self, model, expectedResult, colapsed_columns = False):
        result = svm.datamodel_visualizer(model).draw(colapsed_columns)
        self.assertListEqual(expectedResult,result)

