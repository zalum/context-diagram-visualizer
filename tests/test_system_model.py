import unittest
import system_model

class Test(unittest.TestCase):

    def test_find_isolated_connected_graph(self):
        graph = dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                },
            edges = []
        )

        connected_graph = system_model.system_model(graph).find_connected_graph("product")

        self.assertDictEqual(connected_graph,dict(
            vertexes = {"product":{"type":"product"}},edges=[]
        ))

    def test_find_connected_graph_with_one_level(self):
        graph = dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                },
            edges = [{"start":"product","end":"application1","relation_type":"contains"}]
        )

        connected_graph = system_model.system_model(graph).find_connected_graph("product")

        self.assertDictEqual(connected_graph,dict(
            vertexes = {"product":{"type":"product"},"application1":{"type":"application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"}]
        ))

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

        connected_graph = system_model.system_model(graph).find_connected_graph("product")

        self.assertDictEqual(connected_graph,dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        ))

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

        connected_graph = system_model.system_model(graph).find_connected_graph("product")

        self.assertDictEqual(connected_graph,dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "product", "end": "application2", "relation_type": "contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        ))

    def test_append(self):
        #given
        graph1 = dict(
            vertexes={
                "product": {"type": "product"},
                "application1": {"type": "application"},
                "application2": {"type": "application"}

            },
            edges=[{"start": "product", "end": "application1", "relation_type": "contains"},
                   {"start": "product", "end": "application2", "relation_type": "contains"},
                   {"start": "application1", "end": "application2", "relation_type": "calls"}]
        )
        graph2 = dict(
            vertexes={
                "application2": {"type": "application"},
                "application3": {"type": "application"},

            },
            edges=[{"start": "application3", "end": "application2", "relation_type": "calls"}]
        )

        system_model1 = system_model.system_model(graph1)

        #when
        system_model1.append(system_model.system_model(graph2));


        #then
        expected = dict(
            vertexes={
                "product": {"type": "product"},
                "application1": {"type": "application"},
                "application2": {"type": "application"},
                "application3": {"type": "application"},

            },
            edges=[{"start": "product", "end": "application1", "relation_type": "contains"},
                   {"start": "product", "end": "application2", "relation_type": "contains"},
                   {"start": "application1", "end": "application2", "relation_type": "calls"},
                   {"start": "application3", "end": "application2", "relation_type": "calls"}])

        self.assertDictEqual(system_model1.graph,expected)
