import smv.datamodel_diagram as diagram
from smv.core.model.system_model import data_model
from smv.core.model.system_model import SYSTEM_NODES
from smv.core.model import system_models_repository

import unittest


class DatamodelDiagramTest(unittest.TestCase):
    def test_search_tables_and_users(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user1", "database-user")
        input_model.add_system_node("user2", "database-user")
        input_model.add_system_node("table1", "table")
        input_model.add_system_node("table2", "table")
        input_model.add_system_node("table3", "table")
        input_model.add_system_node("table4", "table")
        # data_model().add_vertex("col1", "column")
        # data_model().add_vertex("col2", "column")
        # data_model().add_vertex("col3", "column")
        input_model.add_relation("user1", "table1", "contains")
        input_model.add_relation("user1", "table2", "uses")
        input_model.add_relation("user2", "table2", "contains")
        input_model.add_relation("user2", "table3", "contains")
        input_model.add_relation("user2", "table4", "contains")
        # data_model().add_edge("table1","col1","contains")
        # data_model().add_edge("table2","col2","contains")
        # data_model().add_edge("table3","col3","contains")
        system_models_repository.set_model(input_model)

        # when
        result = diagram.search_database_user("user1")

        # then
        expected = data_model()
        expected.add_system_node("user1", "database-user")
        expected.add_system_node("user2", "database-user")
        expected.add_system_node("table1", "table")
        expected.add_system_node("table2", "table")
        expected.add_relation("user1", "table1", "contains")
        expected.add_relation("user1", "table2", "uses")
        expected.add_relation("user2", "table2", "contains")
        self.assert_models_are_equal(expected, result)

    def test_search_tables_with_columns_and_fk_and_users(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user1", "database-user")
        input_model.add_system_node("user2", "database-user")
        input_model.add_system_node("table1", "table")
        input_model.add_system_node("table2", "table")
        input_model.add_system_node("table3", "table")
        input_model.add_system_node("table4", "table")
        input_model.add_system_node("col1", "column")
        input_model.add_system_node("col2", "column")
        input_model.add_system_node("col3", "column")
        input_model.add_system_node("col4", "column")
        input_model.add_relation("user1", "table1", "contains")
        input_model.add_relation("user1", "table2", "uses")
        input_model.add_relation("user2", "table2", "contains")
        input_model.add_relation("user2", "table3", "contains")
        input_model.add_relation("user2", "table4", "contains")
        input_model.add_relation("table1", "col1", "contains")
        input_model.add_relation("table2", "col2", "contains")
        input_model.add_relation("table3", "col3", "contains")
        input_model.add_relation("table4", "col4", "contains")
        input_model.add_relation("col1", "col3", "fk")
        system_models_repository.set_model(input_model)

        # when
        result = diagram.search_database_user("user1")

        # then
        expected = data_model()
        expected.add_system_node("user1", "database-user")
        expected.add_system_node("user2", "database-user")
        expected.add_system_node("table1", "table")
        expected.add_system_node("table2", "table")
        expected.add_system_node("table3", "table")
        expected.add_system_node("col1", "column")
        expected.add_system_node("col2", "column")
        expected.add_system_node("col3", "column")
        expected.add_relation("user1", "table1", "contains")
        expected.add_relation("user1", "table2", "uses")
        expected.add_relation("user2", "table2", "contains")
        expected.add_relation("table1", "col1", "contains")
        expected.add_relation("table2", "col2", "contains")
        expected.add_relation("table3", "col3", "contains")
        expected.add_relation("col1", "col3", "fk")
        self.assert_models_are_equal(expected, result)

    def test_search_composition_relation(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user", "database-user")
        input_model.add_system_node("table", "table")
        input_model.add_system_node("part", "table")
        input_model.add_system_node("parts", "column")
        input_model.add_system_node("column_part", "column")
        input_model.add_relation("user", "table", "contains")
        input_model.add_relation("user", "part", "contains")
        input_model.add_relation("table", "parts", "contains")
        input_model.add_relation("part", "parts", "composition")
        input_model.add_relation("column_part", "part", "contains")
        system_models_repository.set_model(input_model)

        # when
        result = diagram.search_database_user("user")

        # then
        self.assert_models_are_equal(input_model, result)

    @unittest.skip("because search criteria does not support matching edge&relation combinations")
    def test_search_tables_excluding_not_targeted_users(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user1", "database-user")
        input_model.add_system_node("user2", "database-user")
        input_model.add_system_node("user3", "database-user")
        input_model.add_system_node("table1", "table")
        input_model.add_system_node("col1", "column")
        input_model.add_relation("user1", "table1", "uses")
        input_model.add_relation("user2", "table1", "contains")
        input_model.add_relation("user3", "table1", "uses")
        input_model.add_relation("col1", "table1", "contains")

        system_models_repository.set_model(input_model)

        # when
        result = diagram.search_database_user("user1")

        # then
        expected = data_model()
        expected.add_system_node("user1", "database-user")
        expected.add_system_node("user2", "database-user")
        expected.add_system_node("user3", "database-user")
        expected.add_system_node("col1", "column")
        expected.add_system_node("table1", "table")
        expected.add_relation("user1", "table1", "uses")
        expected.add_relation("user2", "table1", "contains")
        expected.add_relation("col1", "table1", "contains")
        self.assert_models_are_equal(expected, result)

    def assert_models_are_equal(self, model1: data_model, model2: data_model):
        self.assertDictEqual(model1.graph[SYSTEM_NODES], model2.graph[SYSTEM_NODES])
        self.assertSetEqual(set(hash(frozenset(edge.items())) for edge in model1.get_relations()),
                            set(hash(frozenset(edge.items())) for edge in model2.get_relations()))
