from unittest import TestCase

from smv.core.model.system_model import system_model
from smv.core.model.system_model import SYSTEM_NODES
from smv.core.model.system_model import RELATIONS
from smv.search_model import search_criteria, find_connected_graph


class Test(TestCase):

    def test_find_connected_graph_with_missing_from(self):
        # given
        model = system_model()
        model.add_system_node("1", "application")

        # when
        result = find_connected_graph(model, "2", level=3)

        #then
        self.assert_models_are_equal(system_model(), result)

    def test_find_connected_graph_until_certain_level(self):
        #given
        model = system_model()
        model.add_system_node("1", "application")
        model.add_system_node("2", "application")
        model.add_system_node("3", "application")
        model.add_system_node("4", "application")
        model.add_system_node("5", "application")
        model.add_relation("1", "2")
        model.add_relation("2", "3")
        model.add_relation("3", "4")
        model.add_relation("4", "5")

        #when
        result = find_connected_graph(model,"1",level=3)

        #then
        expected = system_model()
        expected.add_system_node("1", "application")
        expected.add_system_node("2", "application")
        expected.add_system_node("3", "application")
        expected.add_system_node("4", "application")
        expected.add_relation("1", "2")
        expected.add_relation("2", "3")
        expected.add_relation("3", "4")
        self.assert_models_are_equal(expected,result)

    def test_find_isolated_connected_graph(self):
        # given
        graph = dict()
        graph[SYSTEM_NODES]={
            "product": {"type": "product"},
            "application1": {"type": "application"},
        }
        graph[RELATIONS]=[]

        #when
        result = find_connected_graph(system_model(graph),"product")

        #then
        expected = dict()
        expected[SYSTEM_NODES] = {"product": {"type": "product"}}
        expected[RELATIONS] = []
        self.assert_models_are_equal(system_model(expected), result)

    def test_find_connected_graph_with_one_level(self):
        # given
        graph = dict()
        graph[SYSTEM_NODES] = {
            "product":{"type":"product"},
            "application1":{"type":"application"},
            }
        graph[RELATIONS] = [{"start":"product","end":"application1","relation_type":"contains"}]

        # when
        connected_graph = find_connected_graph(system_model(graph),"product")

        #then
        expected = dict()
        expected[SYSTEM_NODES] ={"product": {"type": "product"}, "application1": {"type": "application"}}
        expected[RELATIONS] = [{"start": "product", "end": "application1", "relation_type": "contains"}]
        self.assert_models_are_equal(system_model(expected), connected_graph)

    def test_find_connected_graph_with_multiple_levels(self):
        # given
        graph = dict()
        graph[SYSTEM_NODES] = {
            "product":{"type":"product"},
            "application1":{"type":"application"},
            "application2": {"type": "application"},
            "application3": {"type": "application"},
            }
        graph[RELATIONS] = [{"start":"product","end":"application1","relation_type":"contains"},
                 {"start": "application1", "end": "application2", "relation_type": "calls"}]

        # when
        connected_graph = find_connected_graph(system_model(graph),"product")

        # then
        expected = dict()
        expected[SYSTEM_NODES] = {"product": {"type": "product"}, "application1": {"type": "application"},
                           "application2": {"type": "application"}}
        expected[RELATIONS]=[{"start": "product", "end": "application1", "relation_type": "contains"},
                        {"start": "application1", "end": "application2", "relation_type": "calls"}]
        self.assert_models_are_equal(system_model(expected), connected_graph)

    def test_find_connected_graph_with_corrupted_edge(self):
        # given
        graph = dict()
        graph[SYSTEM_NODES]={
            "product": {"type": "product"},
            "application1": {"type": "application"},
        }
        graph[RELATIONS]=[{"start": "product", "end": "application1", "relation_type": "contains"},
               {"start": "product", "end": "application2", "relation_type": "contains"}]


        model = system_model(graph)

        # when
        result = find_connected_graph(model,"product")

        # then
        expected = system_model()
        expected.add_system_node("product", "product")
        expected.add_system_node("application1", "application")
        expected.add_relation("product", "application1", "contains")
        self.assert_models_are_equal(expected,result)

    def test_find_connected_graph_with_empty_criteria(self):
        #given
        model = system_model()
        model.add_system_node("user", "user")
        model.add_system_node("table1", "table")
        model.add_system_node("schema", "schema")
        model.add_relation("user", "table1", "uses")
        model.add_relation("user", "schema", "uses")

        criteria = search_criteria()

        #when
        result = find_connected_graph(model,"user",criteria)

        #then
        expected = system_model()
        expected.add_system_node("user", "user")
        expected.add_system_node("table1", "table")
        expected.add_system_node("schema", "schema")
        expected.add_relation("user", "table1", "uses")
        expected.add_relation("user", "schema", "uses")
        self.assert_models_are_equal(expected, result)

    def test_find_connected_graph_with_cycle(self):
        graph = dict()
        graph[SYSTEM_NODES] = {
            "product":{"type":"product"},
            "application1":{"type":"application"},
            "application2": {"type": "application"},
            "application3": {"type": "application"},

            }
        graph[RELATIONS] = [{"start":"product","end":"application1","relation_type":"contains"},
                 {"start": "product", "end": "application2", "relation_type": "contains"},
                 {"start": "application1", "end": "application2", "relation_type": "calls"}]

        result = find_connected_graph(system_model(graph),"product")

        expected = dict()
        expected[SYSTEM_NODES] ={"product": {"type": "product"}, "application1": {"type": "application"},
                           "application2": {"type": "application"}}
        expected[RELATIONS]=[{"start": "product", "end": "application1", "relation_type": "contains"},
                        {"start": "product", "end": "application2", "relation_type": "contains"},
                        {"start": "application1", "end": "application2", "relation_type": "calls"}]
        self.assert_models_are_equal(system_model(expected), result)

    def test_search_criteria_by_vertex_type(self):
        #given
        model = system_model()
        model.add_system_node("user", "user")
        model.add_system_node("table1", "table")
        model.add_system_node("schema", "schema")
        model.add_relation("user", "table1", "uses")
        model.add_relation("user", "schema", "uses")

        criteria = search_criteria().with_include_vertex_types(0, ["table"])

        #when
        result = find_connected_graph(model,"user", criteria=criteria)

        #then
        expected = system_model()
        expected.add_system_node("user", "user")
        expected.add_system_node("table1", "table")
        expected.add_relation("user", "table1", "uses")
        self.assertIsNotNone(result)
        self.assert_models_are_equal(expected, result)

    def test_search_criteria_by_multiple_vertex_types(self):
        #given
        model = system_model()
        model.add_system_node("user", "user")
        model.add_system_node("table1", "table")
        model.add_system_node("schema", "schema")
        model.add_system_node("xxx", "xxx")
        model.add_relation("user", "table1", "uses")
        model.add_relation("user", "schema", "uses")
        model.add_relation("user", "xxx", "uses")
        criteria = search_criteria().with_include_vertex_types(0,["table","schema"])

        #when
        result = find_connected_graph(model,"user",criteria=criteria)

        #then
        expected = system_model()
        expected.add_system_node("user", "user")
        expected.add_system_node("table1", "table")
        expected.add_system_node("schema", "schema")
        expected.add_relation("user", "table1", "uses")
        expected.add_relation("user", "schema", "uses")
        self.assertIsNotNone(result)
        self.assert_models_are_equal(expected, result)

    def test_search_criteria_by_relation_type(self):
        #given
        model = system_model()
        model.add_system_node("user", "user")
        model.add_system_node("table1", "table")
        model.add_system_node("schema", "schema")
        model.add_relation("user", "table1", "uses")
        model.add_relation("user", "schema", "xxx")

        criteria = search_criteria().with_include_relation_types(0,["uses"])

        #when
        result = find_connected_graph(model,"user",criteria=criteria)

        #then
        expected = system_model()
        expected.add_system_node("user", "user")
        expected.add_system_node("table1", "table")
        expected.add_relation("user", "table1", "uses")
        self.assertIsNotNone(result)
        self.assert_models_are_equal(expected,result)

    def test_search_criteria_multilevel(self):
        #given
        model = system_model()
        model.add_system_node("user", "user")
        model.add_system_node("table1", "table")
        model.add_system_node("table2", "table")
        model.add_system_node("table3", "table")
        model.add_system_node("column1", "column")
        model.add_system_node("schema", "schema")
        model.add_system_node("column2", "column")
        model.add_relation("user", "table1", "uses")
        model.add_relation("schema", "table1", "contains")
        model.add_relation("schema", "table2", "contains")
        model.add_relation("schema", "table3", "contains")
        model.add_relation("column2", "table2", "contains")
        model.add_relation("column1", "table1", "contains")
        model.add_relation("column2", "column1", "fk")
        #when
        criteria = search_criteria().with_include_vertex_types(0, ["table"]).\
            with_include_vertex_types(1, ["schema","column"]).\
            with_include_relation_types(2, ["fk"])

        #then
        result = find_connected_graph(model,"user", criteria=criteria)
        expected_model = system_model()
        expected_model.add_system_node("user", "user")
        expected_model.add_system_node("table1", "table")
        expected_model.add_system_node("table2", "table")
        expected_model.add_system_node("column1", "column")
        expected_model.add_system_node("schema", "schema")
        expected_model.add_system_node("column2", "column")
        expected_model.add_relation("user", "table1", "uses")
        expected_model.add_relation("schema", "table1", "contains")
        expected_model.add_relation("schema", "table2", "contains")
        expected_model.add_relation("column2", "table2", "contains")
        expected_model.add_relation("column1", "table1", "contains")
        expected_model.add_relation("column2", "column1", "fk")
        self.assert_models_are_equal(result, expected_model)

    def assert_models_are_equal(self, model1:system_model, model2:system_model):
        self.assertDictEqual(model1.graph[SYSTEM_NODES],model2.graph[SYSTEM_NODES])
        self.assertSetEqual(set(hash(frozenset(edge.items())) for edge in model1.get_relations()),
                            set(hash(frozenset(edge.items())) for edge in model2.get_relations()))


