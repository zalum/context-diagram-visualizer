from unittest import TestCase

import smv.core.model.system_models_repository
from smv.core.infrastructure.file_system_model_repository import FileSystemModelsRepository
from smv.core.model.system_model import system_model


class TestCase(TestCase):

    def test_filter(self):
        # given
        model = system_model()
        model.add_system_node("1", "application")
        model.add_system_node("2", "product")
        model.add_system_node("3", "application")
        repo = FileSystemModelsRepository()
        repo.append_system_model(model)

        # when
        result = repo.filter("application")

        # then
        self.assertIn("1", result)
        self.assertNotIn("2", result)
        self.assertIn("3", result)
