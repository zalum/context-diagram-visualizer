import smv.datamodel_diagram as diagram
from smv.system_model import data_model
from smv.system_model_state import state

import unittest

class DatamodelDiagramTest(unittest.TestCase):

    def test_search_tables_and_users(self):
        # given
        input_model = data_model()
        input_model.add_vertex("user1","database-user")
        input_model.add_vertex("user2","database-user")
        input_model.add_vertex("table1","table")
        input_model.add_vertex("table2","table")
        input_model.add_vertex("table3","table")
        input_model.add_vertex("table4","table")
        # data_model().add_vertex("col1", "column")
        # data_model().add_vertex("col2", "column")
        # data_model().add_vertex("col3", "column")
        input_model.add_edge("user1","table1","contains")
        input_model.add_edge("user1","table2","uses")
        input_model.add_edge("user2","table2","contains")
        input_model.add_edge("user2","table3","contains")
        input_model.add_edge("user2","table4","contains")
        # data_model().add_edge("table1","col1","contains")
        # data_model().add_edge("table2","col2","contains")
        # data_model().add_edge("table3","col3","contains")
        state.set_model(input_model)

        # when
        result = diagram.search_database_user("user1")

        #then
        expected = data_model()
        expected.add_vertex("user1", "database-user")
        expected.add_vertex("user2", "database-user")
        expected.add_vertex("table1", "table")
        expected.add_vertex("table2", "table")
        expected.add_edge("user1", "table1", "contains")
        expected.add_edge("user1", "table2", "uses")
        expected.add_edge("user2", "table2", "contains")
        self.assert_models_are_equal(expected,result)

    def test_search_tables_with_columns_and_fk_and_users(self):
        # given
        input_model = data_model()
        input_model.add_vertex("user1","database-user")
        input_model.add_vertex("user2","database-user")
        input_model.add_vertex("table1","table")
        input_model.add_vertex("table2","table")
        input_model.add_vertex("table3","table")
        input_model.add_vertex("table4","table")
        input_model.add_vertex("col1", "column")
        input_model.add_vertex("col2", "column")
        input_model.add_vertex("col3", "column")
        input_model.add_vertex("col4", "column")
        input_model.add_edge("user1","table1","contains")
        input_model.add_edge("user1","table2","uses")
        input_model.add_edge("user2","table2","contains")
        input_model.add_edge("user2","table3","contains")
        input_model.add_edge("user2","table4","contains")
        input_model.add_edge("table1","col1","contains")
        input_model.add_edge("table2","col2","contains")
        input_model.add_edge("table3","col3","contains")
        input_model.add_edge("table4","col4","contains")
        input_model.add_edge("col1","col3","fk")
        state.set_model(input_model)

        # when
        result = diagram.search_database_user("user1")

        #then
        expected = data_model()
        expected.add_vertex("user1", "database-user")
        expected.add_vertex("user2", "database-user")
        expected.add_vertex("table1", "table")
        expected.add_vertex("table2", "table")
        expected.add_vertex("table3", "table")
        expected.add_vertex("col1", "column")
        expected.add_vertex("col2", "column")
        expected.add_vertex("col3", "column")
        expected.add_edge("user1", "table1", "contains")
        expected.add_edge("user1", "table2", "uses")
        expected.add_edge("user2", "table2", "contains")
        expected.add_edge("table1", "col1", "contains")
        expected.add_edge("table2", "col2", "contains")
        expected.add_edge("table3", "col3", "contains")
        expected.add_edge("col1", "col3", "fk")
        self.assert_models_are_equal(expected,result)

    def test_search_tables_excluding_not_targeted_users(self):
        # given
        input_model = data_model()
        input_model.add_vertex("user1","database-user")
        input_model.add_vertex("user2","database-user")
        input_model.add_vertex("user3","database-user")
        input_model.add_vertex("table1","table")
        input_model.add_vertex("col1", "column")
        input_model.add_edge("user1","table1","uses")
        input_model.add_edge("user2","table1","contains")
        input_model.add_edge("user3","table1","uses")
        input_model.add_edge("col1","table1","contains")

        state.set_model(input_model)

        # when
        result = diagram.search_database_user("user1")

        #then
        expected = data_model()
        expected.add_vertex("user1","database-user")
        expected.add_vertex("user2","database-user")
        expected.add_vertex("user3","database-user")
        expected.add_vertex("col1", "column")
        expected.add_vertex("table1","table")
        expected.add_edge("user1","table1","uses")
        expected.add_edge("user2","table1","contains")
        expected.add_edge("col1","table1","contains")
        self.assert_models_are_equal(expected,result)


    def assert_models_are_equal(self, model1: data_model, model2: data_model):
        self.assertDictEqual(model1.graph["vertexes"],model2.graph["vertexes"])
        self.assertSetEqual(set(hash(frozenset(edge.items())) for edge in model1.graph["edges"]),
                            set(hash(frozenset(edge.items())) for edge in model2.graph["edges"]))


