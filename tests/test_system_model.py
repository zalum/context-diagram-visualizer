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

        self.assertDictEqual(connected_graph.graph,dict(
            vertexes = {"product":{"type":"product"}},edges=[]
        ))

    def test_find_one_level_connected_graph(self):
        graph = dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                },
            edges = [{"start":"product","end":"application1","relation_type":"contains"}]
        )

        connected_graph = system_model.system_model(graph).find_connected_graph("product")

        self.assertDictEqual(connected_graph.graph,dict(
            vertexes = {"product":{"type":"product"},"application1":{"type":"application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"}]
        ))

    def test_find_multiple_level_connected_graph(self):
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

        self.assertDictEqual(connected_graph.graph,dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        ))

    def test_find_cycle_connected_graph(self):
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

        self.assertDictEqual(connected_graph.graph,dict(
            vertexes = {
                "product":{"type":"product"},
                "application1":{"type":"application"},
                "application2": {"type": "application"}},
            edges=[{"start":"product","end":"application1","relation_type":"contains"},
                     {"start": "product", "end": "application2", "relation_type": "contains"},
                     {"start": "application1", "end": "application2", "relation_type": "calls"}]
        ))
