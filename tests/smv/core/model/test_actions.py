import unittest

from smv.core.model.system_model import system_model

from smv.core.model.application_config import config
config["persistance-engine"] = "file-system"
from smv.core.model import load_context
load_context()
from smv.core.model import system_models_repository
from smv.core.actions import find_direct_connections


class Test(unittest.TestCase):

    def test_find_direct_connections(self):
        # given
        model = system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_relation("v1", "v2", "contains")
        system_models_repository.set_model(model)

        # when
        result = find_direct_connections("v1")

        # then
        self.assertIsNotNone(result)
        self.assertIn("v2", result)


    def test_find_direct_connections_of_vertex_type(self):
        # given
        model = system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_system_node("v3", "database-user")
        model.add_system_node("v4", "application")
        model.add_system_node("v5", "application")
        model.add_relation("v1", "v2", "contains")
        model.add_relation("v1", "v4", "contains")
        model.add_relation("v1", "v3", "uses")
        system_models_repository.set_model(model)

        # when
        result = find_direct_connections("v1", "application")

        # then
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn("v2", result)
        self.assertIn("v4", result)

    @unittest.skip("SearchCriteria does not support match of node and relation type at the same time")
    def test_find_direct_connections_of_vertex_and_relation_type(self):
        # given
        model = system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_system_node("v3", "database-user")
        model.add_system_node("v4", "application")
        model.add_system_node("v5", "application")
        model.add_relation("v1", "v2", "contains")
        model.add_relation("v1", "v4", "contains")
        model.add_relation("v1", "v5", "calls")
        model.add_relation("v1", "v3", "uses")
        system_models_repository.set_model(model)

        # when
        result = find_direct_connections("v1", "application", "contains")

        # then
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIn("v2", result)
        self.assertIn("v4", result)

    def test_find_direct_connections_of_relation_type(self):
        # given
        model = system_model()
        model.add_system_node("v1", "product")
        model.add_system_node("v2", "application")
        model.add_system_node("v3", "database-user")
        model.add_system_node("v4", "application")
        model.add_system_node("v5", "application")
        model.add_relation("v1", "v2", "contains")
        model.add_relation("v1", "v4", "contains")
        model.add_relation("v1", "v5", "calls")
        model.add_relation("v1", "v3", "contains")
        system_models_repository.set_model(model)

        # when
        result = find_direct_connections("v1", relation_type="contains")

        # then
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertIn("v2", result)
        self.assertIn("v3", result)
        self.assertIn("v4", result)
