import unittest

from smv.core.model import system_model
from smv.core.model.system_model import SYSTEM_NODES
from smv.core.model.system_model import RELATIONS

from smv.core import *


class Test(unittest.TestCase):

    def test_constructor_when_default_parameter_is_mutated(self):
        """
        http://docs.python-guide.org/en/latest/writing/gotchas/
        """
        # given
        model = system_model.system_model()
        model.add_system_node("SCHEMA1", "database-user")

        # when
        model = system_model.system_model()

        # then
        self.assertDictEqual(model.graph,system_model.empty_graph())

    def test_copy_vertex(self):
        # given
        model_source = system_model.system_model()
        model_source.add_system_node("1", "application", x=1, y=2)
        model_target = system_model.system_model()

        # when
        model_target.copy_system_node(model_source, "1")

        # then
        self.assertDictEqual(model_target.get_system_node("1"), model_source.get_system_node("1"))

    def test_add_vertex(self):
        # given
        model = system_model.system_model()
        properties = dict(name="xxx",other="yyy")

        # when
        response = model.add_system_node("1", "app", **properties)
        properties["name"] = "zzz"

        # then
        self.assertEquals(response.return_code, RESPONSE_OK)
        properties["type"] = "app"
        properties["name"] = "xxx"
        self.assertEquals(response.content, {"1":properties})
        expected = dict(name="xxx",other="yyy",type = "app")
        self.assertDictEqual(expected, model.get_system_node("1"))

    def test_add_vertex_with_existing_node(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", type="application")

        # when
        result = model.add_system_node("1", type="application")

        # then
        self.assertEquals(result.return_code,RESPONSE_ERROR)
        self.assertEquals(result.content,"System Node '1' already exists")


    def test_find_direct_connections(self):
        # given
        model = system_model.system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_relation("v1", "v2", "contains")

        # when
        result = model.find_direct_connections("v1")

        # then
        self.assertIsNotNone(result)
        self.assertIn("v2",result)


    def test_find_direct_connections_of_vertex_type(self):
        # given
        model = system_model.system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_system_node("v3", "database-user")
        model.add_system_node("v4", "application")
        model.add_system_node("v5", "application")
        model.add_relation("v1", "v2", "contains")
        model.add_relation("v1", "v4", "contains")
        model.add_relation("v1", "v3", "uses")

        # when
        result = model.find_direct_connections("v1","application")

        # then
        self.assertIsNotNone(result)
        self.assertEqual(len(result),2)
        self.assertIn("v2",result)
        self.assertIn("v4",result)

    def test_find_direct_connections_of_vertex_and_relation_type(self):
        # given
        model = system_model.system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_system_node("v3", "database-user")
        model.add_system_node("v4", "application")
        model.add_system_node("v5", "application")
        model.add_relation("v1", "v2", "contains")
        model.add_relation("v1", "v4", "contains")
        model.add_relation("v1", "v5", "calls")
        model.add_relation("v1", "v3", "uses")

        # when
        result = model.find_direct_connections("v1","application","contains")

        # then
        self.assertIsNotNone(result)
        self.assertEqual(len(result),2)
        self.assertIn("v2",result)
        self.assertIn("v4",result)

    def test_find_direct_connections_of_relation_type(self):
        # given
        model = system_model.system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_system_node("v3", "database-user")
        model.add_system_node("v4", "application")
        model.add_system_node("v5", "application")
        model.add_relation("v1", "v2", "contains")
        model.add_relation("v1", "v4", "contains")
        model.add_relation("v1", "v5", "calls")
        model.add_relation("v1", "v3", "contains")

        # when
        result = model.find_direct_connections("v1",relation_type="contains")

        # then
        self.assertIsNotNone(result)
        self.assertEqual(len(result),3)
        self.assertIn("v2",result)
        self.assertIn("v3",result)
        self.assertIn("v4",result)

    def test_append(self):
        # given
        graph1 = dict()
        graph1[SYSTEM_NODES]={
            "product": {"type": "product"},
            "application1": {"type": "application"},
            "application2": {"type": "application"}

        }
        graph1[RELATIONS]=[{"start": "product", "end": "application1", "relation_type": "contains"},
               {"start": "product", "end": "application2", "relation_type": "contains"},
               {"start": "application1", "end": "application2", "relation_type": "calls"}]
        graph2 = dict()
        graph2[SYSTEM_NODES] = {
            "application2": {"type": "application"},
            "application3": {"type": "application"},

        }
        graph2[RELATIONS] = [{"start": "application3", "end": "application2", "relation_type": "calls"}]
        system_model1 = system_model.system_model(graph1)

        # when
        system_model1.append(system_model.system_model(graph2))

        # then
        expected = dict()
        expected[SYSTEM_NODES]={
            "product": {"type": "product"},
            "application1": {"type": "application"},
            "application2": {"type": "application"},
            "application3": {"type": "application"},

        }
        expected[RELATIONS]=[{"start": "product", "end": "application1", "relation_type": "contains"},
               {"start": "product", "end": "application2", "relation_type": "contains"},
               {"start": "application1", "end": "application2", "relation_type": "calls"},
               {"start": "application3", "end": "application2", "relation_type": "calls"}]

        self.assertDictEqual(system_model1.graph,expected)

    def test_append_duplicated_edges(self):
        # given
        model1 = system_model.system_model()
        model1.add_system_node("1", "product")
        model1.add_system_node("2", "product")
        model1.add_relation("1", "2", "uses")

        model2 = system_model.system_model()
        model2.add_system_node("1", "product")
        model2.add_system_node("2", "product")
        model2.add_system_node("3", "product")
        model2.add_relation("1", "2", "uses")
        model2.add_relation("1", "3", "uses")

        # when
        model1.append(model2)

        # then
        expected = system_model.system_model()
        expected.add_system_node("1", "product")
        expected.add_system_node("2", "product")
        expected.add_system_node("3", "product")
        expected.add_relation("1", "2", "uses")
        expected.add_relation("1", "3", "uses")

        self.assertEquals(expected.graph,expected.graph)

    def test_append_edges_with_no_relation_type(self):
        # given
        model1 = system_model.system_model()
        model1.add_system_node("1", "product")
        model1.add_system_node("2", "product")
        model1.add_relation("1", "2", "uses")

        model2 = system_model.system_model()
        model2.add_system_node("1", "product")
        model2.add_system_node("2", "product")
        model2.add_system_node("3", "product")
        model2.add_relation("1", "3")

        # when
        model1.append(model2)

        # then
        expected = system_model.system_model()
        expected.add_system_node("1", "product")
        expected.add_system_node("2", "product")
        expected.add_system_node("3", "product")
        expected.add_relation("1", "2", "uses")
        expected.add_relation("1", "3")

        self.assertEquals(model1.graph,expected.graph)

    def test_add_relation_with_missing_node(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", "product")

        # when
        result = model.add_relation("1", "2", "fk")

        # then
        self.assertEquals(result.return_code, RESPONSE_ERROR)
        self.assertEquals(result.content, "End node '2' is not in the model")


    def test_add_edge_duplication(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", "product")
        model.add_system_node("2", "application")
        model.add_relation("1", "2", "fk")

        # when
        result = model.add_relation("1", "2", "fk")

        # then
        self.assertEquals(result.return_code, RESPONSE_ERROR)
        self.assertEquals(len(model.get_relations()), 1)

    def test_add_edge_duplication_with_no_relation_type(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", "product")
        model.add_system_node("2", "application")
        model.add_relation("1", "2")

        # when
        result = model.add_relation("1", "2")

        # then
        self.assertEquals(result.return_code, RESPONSE_ERROR)
        self.assertEquals(len(model.get_relations()), 1)

    def test_add_edge_duplication_with_different_relation_type(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", "product")
        model.add_system_node("2", "application")
        model.add_relation("1", "2", "fk")

        # when
        result = model.add_relation("1", "2", "uses")

        # then
        self.assertEquals(result.return_code, RESPONSE_OK)
        self.assertEquals(len(model.get_relations()), 2)
        self.assertEquals(len(model.get_relations_of_type("fk")), 1)
        self.assertEquals(len(model.get_relations_of_type("uses")), 1)

    def test_add_edge_with_corrupted_model(self):
        # given
        graph = {
            SYSTEM_NODES : {"1":{},"2":{}},
            RELATIONS: [{"start":"1","end":"2"}, {"start":"1","end":"2"}]
        }

        model = system_model.system_model(graph)

        # when
        result = model.add_relation("1", "2")

        # then
        self.assertEquals(result.return_code, RESPONSE_ERROR)
        self.assertEquals(result.content,"more then one edge (2) found for (start=1 end=2 relation_type=None)")

    def test_remove_edge(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", "app")
        model.add_system_node("2", "app")
        model.add_relation(start="1", end="2", relation_type="some_1")
        model.add_relation(start="1", end="2", relation_type="some_2")

        # when
        response = model.remove_relation(start="1", end="2", relation_type="some_1")

        # then
        self.assertEquals(response.return_code, RESPONSE_OK)
        self.assertEquals(len(model.get_relations()), 1)

    def test_remove_missing_edge(self):
        # given
        model = system_model.system_model()
        model.add_system_node("1", "app")
        model.add_system_node("2", "app")
        model.add_relation(start="1", end="2", relation_type="some_2")

        # when
        response = model.remove_relation(start="1", end="2", relation_type="some_1")

        # then
        self.assertEquals(response.return_code, RESPONSE_ERROR)
        self.assertEquals(len(model.get_relations()), 1)


