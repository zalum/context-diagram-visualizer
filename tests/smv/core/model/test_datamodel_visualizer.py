import unittest

import smv.core.model.system_model as sm
from smv.core.model.system_model import DatamodelRelationTypes
from smv.core.model import system_model_visualizer as svm
from sms import nodes
from sms import relations


class DataModelVisualiserTest(unittest.TestCase):

    def test_draw_empty_database_user(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)

        expected_result = ["@startuml", "left to right direction", "@enduml"]
        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result)

    def test_draw_database_user_with_table(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_system_node("TABLE2", type=nodes.table)
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="TABLE2", end="SCHEMA1", relation_type=relations.contains)

        expected_result = ["@startuml", "left to right direction",
                           "package \"SCHEMA1\"{",
                           "class TABLE1 {", "}",
                           "class TABLE2 {", "}",
                           "}",
                           "@enduml"]
        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result)

    def test_start_database_user_end_table_relation(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_relation("SCHEMA1", "TABLE1", relations.contains)
        expected_result = ["@startuml", "left to right direction",
                           "package \"SCHEMA1\"{",
                           "class TABLE1 {", "}",
                           "}",
                           "@enduml"]
        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result)

    def test_draw_table_with_column(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_system_node("T1_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="TABLE1", relation_type=relations.contains)

        expected_result = ["@startuml", "left to right direction", "package \"SCHEMA1\"{", "class TABLE1 {", "+ T1_ID",
                           "}", "}", "@enduml"]
        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result)

    def test_draw_table_with_colapsed_column(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_system_node("T1_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="TABLE1", relation_type=relations.contains)
        expected_result = ["@startuml", "left to right direction", "package \"SCHEMA1\"{", "class TABLE1 {", "}", "}",
                           "@enduml"]
        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result, True)

    def test_draw_foreign_key(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_system_node("TABLE2", type=nodes.table)
        model.add_system_node("T1_ID", type="column")
        model.add_system_node("T2_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="TABLE2", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="TABLE1", relation_type=relations.contains)
        model.add_relation(start="T2_ID", end="TABLE2", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="T2_ID", relation_type=relations.foreign_key)

        expected_result = ["@startuml", "left to right direction", "package \"SCHEMA1\"{",
                           "class TABLE1 {",
                           "+ T1_ID",
                           "}",
                           "class TABLE2 {",
                           "+ T2_ID",
                           "}",
                           "}",
                           "TABLE1::T1_ID --> TABLE2::T2_ID", "@enduml"
                           ]

        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result)

    def test_draw_table_with_colapsed_column_with_fk(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_system_node("TABLE2", type=nodes.table)
        model.add_system_node("T1_ID", type="column")
        model.add_system_node("T2_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="TABLE2", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="TABLE1", relation_type=relations.contains)
        model.add_relation(start="T2_ID", end="TABLE2", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="T2_ID", relation_type=relations.foreign_key)

        expected_result = ["@startuml", "left to right direction", "package \"SCHEMA1\"{",
                           "class TABLE1 {",
                           "}",
                           "class TABLE2 {",
                           "}",
                           "}",
                           "TABLE1 --> TABLE2 : T1_ID::T2_ID", "@enduml"
                           ]

        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result, colapsed_columns=True)

    def test_draw_database_user_uses_tables(self):
        # given
        model = sm.data_model()
        model.add_system_node("user1", nodes.database_user)
        model.add_system_node("schema", nodes.database_user)
        model.add_system_node(nodes.table, nodes.table)
        model.add_system_node("c1", "column")
        model.add_relation("user1", nodes.table, "uses")
        model.add_relation("schema", nodes.table, relations.contains)
        model.add_relation("c1", nodes.table, relations.contains)

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

        self.__run_draw_datamodel_test__(model, "schema", expected)

    def transform_in_lines(self, text: str):
        return list(
            filter(lambda line: False if line == '' else True,
                   map(lambda line: line.lstrip(" "), text.split("\n"))))

    def test_draw_fk_over_two_database_user(self):
        model = sm.data_model()
        model.add_system_node("SCHEMA1", type=nodes.database_user)
        model.add_system_node("SCHEMA2", type=nodes.database_user)
        model.add_system_node("TABLE1", type=nodes.table)
        model.add_system_node("TABLE2", type=nodes.table)
        model.add_system_node("T1_ID", type="column")
        model.add_system_node("T2_ID", type="column")
        model.add_relation(start="TABLE1", end="SCHEMA1", relation_type=relations.contains)
        model.add_relation(start="TABLE2", end="SCHEMA2", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="TABLE1", relation_type=relations.contains)
        model.add_relation(start="T2_ID", end="TABLE2", relation_type=relations.contains)
        model.add_relation(start="T1_ID", end="T2_ID", relation_type=relations.foreign_key)

        expected_result = ["@startuml", "left to right direction", "package \"SCHEMA1\"{",
                           "class TABLE1 {",
                           "+ T1_ID",
                           "}",
                           "}",
                           "package \"SCHEMA2\"{",
                           "class TABLE2 {",
                           "+ T2_ID",
                           "}",
                           "}",
                           "TABLE1::T1_ID --> TABLE2::T2_ID", "@enduml"
                           ]
        self.__run_draw_datamodel_test__(model, "SCHEMA1", expected_result)

    def test_composition_relation_on_column(self):
        # given
        datamodel = sm.data_model()
        datamodel.add_system_node("aggregate_root", type=nodes.table)
        datamodel.add_system_node("user", type=nodes.database_user)
        datamodel.add_system_node("part", type=nodes.table)
        datamodel.add_system_node("parts", type="column")
        datamodel.add_relation(start="aggregate_root", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="parts", end="aggregate_root", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="parts", relation_type=relations.composition)

        # then
        expected_result = self.transform_in_lines("""
        @startuml
        left to right direction
        package "user"{
        class aggregate_root {
        + parts
        }
        class part {
        }
        }
        part --* aggregate_root::parts
        @enduml
        """)

        self.__run_draw_datamodel_test__(datamodel, "user", expected_result)

    def test_composition_relation_with_inverse_relation_direction(self):
        # given
        datamodel = sm.data_model()
        datamodel.add_system_node("aggregate_root", type=nodes.table)
        datamodel.add_system_node("user", type=nodes.database_user)
        datamodel.add_system_node("part", type=nodes.table)
        datamodel.add_system_node("parts", type="column")
        datamodel.add_relation(start="aggregate_root", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="parts", relation_type=relations.composition)
        datamodel.add_relation(start="part", end="user", relation_type=relations.contains)
        datamodel.add_relation(end="parts", start="aggregate_root", relation_type=relations.contains)

        # then
        expected_result = self.transform_in_lines("""
        @startuml
        left to right direction
        package "user"{
        class aggregate_root {
        + parts
        }
        class part {
        }
        }
        part --* aggregate_root::parts
        @enduml
        """)

        self.__run_draw_datamodel_test__(datamodel, "user", expected_result)

    def test_composition_relation_on_colapsed_column(self):
        # given
        datamodel = sm.data_model()
        datamodel.add_system_node("aggregate_root", type=nodes.table)
        datamodel.add_system_node("user", type=nodes.database_user)
        datamodel.add_system_node("part", type=nodes.table)
        datamodel.add_system_node("parts", type="column")
        datamodel.add_relation(start="aggregate_root", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="parts", end="aggregate_root", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="parts", relation_type=relations.composition)

        # then
        expected_result = self.transform_in_lines("""
        @startuml
        left to right direction
        package "user"{
        class aggregate_root {
        }
        class part {
        }
        }
        part --* aggregate_root
        @enduml
        """)

        self.__run_draw_datamodel_test__(datamodel, "user", expected_result, colapsed_columns=True)

    def test_composition_relation_on_table(self):
        # given
        datamodel = sm.data_model()
        datamodel.add_system_node("aggregate_root", type=nodes.table)
        datamodel.add_system_node("user", type=nodes.database_user)
        datamodel.add_system_node("part", type=nodes.table)
        datamodel.add_relation(start="aggregate_root", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="user", relation_type=relations.contains)
        datamodel.add_relation(start="part", end="aggregate_root", relation_type=relations.composition)

        # then
        expected_result = self.transform_in_lines("""
        @startuml
        left to right direction
        package "user"{
        class aggregate_root {
        }
        class part {
        }
        }
        part --* aggregate_root
        @enduml
        """)

        self.__run_draw_datamodel_test__(datamodel, "user", expected_result)

    def test_table_with_id(self):
        # given
        datamodel = sm.data_model()
        datamodel.add_system_node("table_1", type=nodes.table, name="table 1")
        datamodel.add_system_node("schema1", type=nodes.database_user)
        datamodel.add_relation("schema1", "table_1", relations.contains)

        # then
        expected_result = ["@startuml",
                           "left to right direction",
                           "package \"schema1\"{",
                           "class \"table 1\" as table_1 {",
                           "}",
                           "}",
                           "@enduml"]

        self.__run_draw_datamodel_test__(datamodel, "user", expected_result)

    def __run_draw_datamodel_test__(self, model, database_user, expectedResult, colapsed_columns=False):
        result = svm.DatamodelVisualizer(model).draw(database_user, colapsed_columns)
        self.assertListEqual(expectedResult, result)
