import unittest

from smv import system_model


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

    def test_find_direct_connections(self):
        #given
        model = system_model.system_model()
        model.add_vertex("v1", "product")
        model.add_vertex("v2", "application")
        model.add_edge("v1","v2","contains")

        #when
        result = model.find_direct_connections("v1")

        #then
        self.assertIsNotNone(result)
        self.assertIn("v2",result)


    def test_find_direct_connections_of_vertex_type(self):
        #given
        model = system_model.system_model()
        model.add_vertex("v1", "product")
        model.add_vertex("v2", "application")
        model.add_vertex("v3", "database-user")
        model.add_vertex("v4", "application")
        model.add_vertex("v5", "application")
        model.add_edge("v1","v2","contains")
        model.add_edge("v1","v4","contains")
        model.add_edge("v1","v3","uses")

        #when
        result = model.find_direct_connections("v1","application")

        #then
        self.assertIsNotNone(result)
        self.assertEqual(len(result),2)
        self.assertIn("v2",result)
        self.assertIn("v4",result)

    def test_find_direct_connections_of_vertex_and_relation_type(self):
        #given
        model = system_model.system_model()
        model.add_vertex("v1", "product")
        model.add_vertex("v2", "application")
        model.add_vertex("v3", "database-user")
        model.add_vertex("v4", "application")
        model.add_vertex("v5", "application")
        model.add_edge("v1","v2","contains")
        model.add_edge("v1","v4","contains")
        model.add_edge("v1","v5","calls")
        model.add_edge("v1","v3","uses")

        #when
        result = model.find_direct_connections("v1","application","contains")

        #then
        self.assertIsNotNone(result)
        self.assertEqual(len(result),2)
        self.assertIn("v2",result)
        self.assertIn("v4",result)

    def test_find_direct_connections_of_relation_type(self):
        #given
        model = system_model.system_model()
        model.add_vertex("v1", "product")
        model.add_vertex("v2", "application")
        model.add_vertex("v3", "database-user")
        model.add_vertex("v4", "application")
        model.add_vertex("v5", "application")
        model.add_edge("v1","v2","contains")
        model.add_edge("v1","v4","contains")
        model.add_edge("v1","v5","calls")
        model.add_edge("v1","v3","contains")

        #when
        result = model.find_direct_connections("v1",relation_type="contains")

        #then
        self.assertIsNotNone(result)
        self.assertEqual(len(result),3)
        self.assertIn("v2",result)
        self.assertIn("v3",result)
        self.assertIn("v4",result)

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

    def test_append_duplicated_edges(self):
        #given
        model1 = system_model.system_model()
        model1.add_vertex("1","product")
        model1.add_vertex("2","product")
        model1.add_edge("1","2","uses")

        model2 = system_model.system_model()
        model2.add_vertex("1","product")
        model2.add_vertex("2","product")
        model2.add_vertex("3","product")
        model2.add_edge("1","2","uses")
        model2.add_edge("1","3","uses")

        #when
        model1.append(model2)

        #then
        expected = system_model.system_model()
        expected.add_vertex("1", "product")
        expected.add_vertex("2", "product")
        expected.add_vertex("3", "product")
        expected.add_edge("1", "2", "uses")
        expected.add_edge("1", "3", "uses")

        self.assertEquals(model1.graph,expected.graph)



    def test_add_edge_duplication(self):
        #given
        model = system_model.system_model()
        model.add_vertex("1","product")
        model.add_vertex("2","application")
        model.add_edge("1","2","fk")

        #when
        result = model.add_edge("1", "2","fk")

        #then
        self.assertEquals(result, system_model.RESPONSE_OK)
        self.assertEquals(len(model.get_edges()),1)

    def test_add_edge_duplication_with_no_relation_type(self):
        #given
        model = system_model.system_model()
        model.add_vertex("1","product")
        model.add_vertex("2","application")
        model.add_edge("1","2")

        #when
        result = model.add_edge("1", "2")

        #then
        self.assertEquals(result, system_model.RESPONSE_OK)
        self.assertEquals(len(model.get_edges()),1)

    def test_add_edge_duplication(self):
        #given
        model = system_model.system_model()
        model.add_vertex("1","product")
        model.add_vertex("2","application")
        model.add_edge("1","2","fk")

        #when
        result = model.add_edge("1", "2","uses")

        #then
        self.assertEquals(result, system_model.RESPONSE_OK)
        self.assertEquals(len(model.get_edges()),2)
        self.assertEquals(len(model.get_edges_of_type("fk")),1)
        self.assertEquals(len(model.get_edges_of_type("uses")),1)

    def test_add_edge_with_corrupted_model(self):
        #given
        graph = dict(vertexes = {"1":{},"2":{}}, edges=[{"start":"1","end":"2"},{"start":"1","end":"2"}])


        model = system_model.system_model(graph)

        #when
        result = model.add_edge("1", "2")

        #then
        self.assertNotEquals(result,system_model.RESPONSE_OK)
        self.assertEquals(result,"more then one edge (2) found for (start=1 end=2 relation_type=None)")


