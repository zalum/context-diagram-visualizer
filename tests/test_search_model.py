from smv.system_model import system_model
from smv.search_model import search_criteria, find_connected_graph
from unittest import TestCase


class Test(TestCase):
    def test_find_connected_graph_until_certain_level(self):
        #given
        model = system_model()
        model.add_vertex("1","application")
        model.add_vertex("2","application")
        model.add_vertex("3","application")
        model.add_vertex("4","application")
        model.add_vertex("5","application")
        model.add_edge("1","2")
        model.add_edge("2","3")
        model.add_edge("3","4")
        model.add_edge("4","5")

        #when
        result = find_connected_graph(model,"1",level=3)

        #then
        expected = system_model()
        expected.add_vertex("1","application")
        expected.add_vertex("2","application")
        expected.add_vertex("3","application")
        expected.add_vertex("4","application")
        expected.add_edge("1","2")
        expected.add_edge("2","3")
        expected.add_edge("3","4")
        self.assert_models_are_equal(expected,result)

    def test_find_isolated_connected_graph(self):
        graph = dict(
            vertexes={
                "product": {"type": "product"},
                "application1": {"type": "application"},
            },
            edges=[]
        )

        result = find_connected_graph(system_model(graph),"product")

        self.assert_models_are_equal(system_model(dict(
            vertexes={"product": {"type": "product"}}, edges=[]
        )),result)

    def test_find_connected_graph_with_one_level(self):
        graph = dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                },
            edges = [{"start":"product","end":"application1","relation_type":"contains"}]
        )

        connected_graph = find_connected_graph(system_model(graph),"product")

        self.assert_models_are_equal(system_model(dict(
            vertexes = {"product":{"type":"product"},"application1":{"type":"application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"}]
        )),connected_graph)

    def test_find_connected_graph_with_multiple_levels(self):
        graph = dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"},
                "application3": {"type": "application"},
                },
            edges = [{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        )

        connected_graph = find_connected_graph(system_model(graph),"product")
        self.assert_models_are_equal(system_model(dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        )),connected_graph)

    def test_find_connected_graph_with_corrupted_edge(self):
        #given
        graph = dict(
            vertexes={
                "product": {"type": "product"},
                "application1": {"type": "application"},
            },
            edges=[{"start": "product", "end": "application1", "relation_type": "contains"},
                   {"start": "product", "end": "application2", "relation_type": "contains"}]
        )

        model = system_model(graph)

        #when
        result = find_connected_graph(model,"product")

        #then
        expected = system_model()
        expected.add_vertex("product","product")
        expected.add_vertex("application1","application")
        expected.add_edge("product","application1","contains")
        self.assert_models_are_equal(expected,result)

    def test_find_connected_graph_with_empty_criteria(self):
        #given
        model = system_model()
        model.add_vertex("user","user")
        model.add_vertex("table1","table")
        model.add_vertex("schema","schema")
        model.add_edge("user","table1","uses")
        model.add_edge("user","schema","uses")

        criteria = search_criteria()

        #when
        result = find_connected_graph(model,"user",criteria)

        #then
        expected = system_model()
        expected.add_vertex("user", "user")
        expected.add_vertex("table1", "table")
        expected.add_vertex("schema", "schema")
        expected.add_edge("user", "table1", "uses")
        expected.add_edge("user", "schema", "uses")
        self.assert_models_are_equal(expected, result)

    def test_find_connected_graph_with_cycle(self):
        graph = dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"},
                "application3": {"type": "application"},

                },
            edges = [{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "product", "end": "application2", "relation_type": "contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        )

        result = find_connected_graph(system_model(graph),"product")

        self.assert_models_are_equal(system_model(dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "product", "end": "application2", "relation_type": "contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        )),result)

    def test_search_criteria_by_vertex_type(self):
        #given
        model = system_model()
        model.add_vertex("user","user")
        model.add_vertex("table1","table")
        model.add_vertex("schema","schema")
        model.add_edge("user","table1","uses")
        model.add_edge("user","schema","uses")

        criteria = search_criteria().with_include_vertex_types(0, ["table"])

        #when
        result = find_connected_graph(model,"user", criteria=criteria)

        #then
        expected = system_model()
        expected.add_vertex("user", "user")
        expected.add_vertex("table1", "table")
        expected.add_edge("user", "table1", "uses")
        self.assertIsNotNone(result)
        self.assert_models_are_equal(expected, result)

    def test_search_criteria_by_multiple_vertex_types(self):
        #given
        model = system_model()
        model.add_vertex("user","user")
        model.add_vertex("table1","table")
        model.add_vertex("schema","schema")
        model.add_vertex("xxx","xxx")
        model.add_edge("user","table1","uses")
        model.add_edge("user","schema","uses")
        model.add_edge("user","xxx","uses")
        criteria = search_criteria().with_include_vertex_types(0,["table","schema"])

        #when
        result = find_connected_graph(model,"user",criteria=criteria)

        #then
        expected = system_model()
        expected.add_vertex("user", "user")
        expected.add_vertex("table1", "table")
        expected.add_vertex("schema", "schema")
        expected.add_edge("user", "table1", "uses")
        expected.add_edge("user", "schema", "uses")
        self.assertIsNotNone(result)
        self.assert_models_are_equal(expected, result)

    def test_search_criteria_by_relation_type(self):
        #given
        model = system_model()
        model.add_vertex("user","user")
        model.add_vertex("table1","table")
        model.add_vertex("schema","schema")
        model.add_edge("user","table1","uses")
        model.add_edge("user","schema","xxx")

        criteria = search_criteria().with_include_relation_types(0,["uses"])

        #when
        result = find_connected_graph(model,"user",criteria=criteria)

        #then
        expected = system_model()
        expected.add_vertex("user", "user")
        expected.add_vertex("table1", "table")
        expected.add_edge("user", "table1", "uses")
        self.assertIsNotNone(result)
        self.assert_models_are_equal(expected,result)

    def test_search_criteria_multilevel(self):
        #given
        model = system_model()
        model.add_vertex("user","user")
        model.add_vertex("table1","table")
        model.add_vertex("table2","table")
        model.add_vertex("table3","table")
        model.add_vertex("column1","column")
        model.add_vertex("schema","schema")
        model.add_vertex("column2","column")
        model.add_edge("user","table1","uses")
        model.add_edge("schema","table1","contains")
        model.add_edge("schema","table2","contains")
        model.add_edge("schema","table3","contains")
        model.add_edge("column2","table2","contains")
        model.add_edge("column1","table1","contains")
        model.add_edge("column2","column1","fk")
        #when
        criteria = search_criteria().with_include_vertex_types(0, ["table"]).\
            with_include_vertex_types(1, ["schema","column"]).\
            with_include_relation_types(2, ["fk"])

        #then
        result = find_connected_graph(model,"user", criteria=criteria)
        expected_model = system_model()
        expected_model.add_vertex("user", "user")
        expected_model.add_vertex("table1", "table")
        expected_model.add_vertex("table2", "table")
        expected_model.add_vertex("column1", "column")
        expected_model.add_vertex("schema", "schema")
        expected_model.add_vertex("column2", "column")
        expected_model.add_edge("user", "table1", "uses")
        expected_model.add_edge("schema", "table1", "contains")
        expected_model.add_edge("schema", "table2", "contains")
        expected_model.add_edge("column2", "table2", "contains")
        expected_model.add_edge("column1", "table1", "contains")
        expected_model.add_edge("column2", "column1", "fk")
        self.assert_models_are_equal(result, expected_model)

    def assert_models_are_equal(self, model1:system_model, model2:system_model):
        self.assertDictEqual(model1.graph["vertexes"],model2.graph["vertexes"])
        self.assertSetEqual(set(hash(frozenset(edge.items())) for edge in model1.graph["edges"]),
                            set(hash(frozenset(edge.items())) for edge in model2.graph["edges"]))


