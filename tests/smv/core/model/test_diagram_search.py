import unittest
import importlib

from smv.core.model import SystemModelsRepository
import smv.core.model.diagram_search as diagram_search
from smv.core.model.system_model import DatamodelRelationTypes
from smv.core.model.system_model import SYSTEM_NODES
from smv.core.model.system_model import component_model
from smv.core.model.system_model import data_model
from sms.schema import nodes

system_models_repository = None  # type:SystemModelsRepository


def reload_system_model_repository()->SystemModelsRepository:
    from smv.core.model.application_config import config, PERSISTANCE_ENGINE, FILE_SYSTEM_DB
    config[PERSISTANCE_ENGINE] = FILE_SYSTEM_DB
    from smv.core.model import load_context
    load_context()
    from smv.core.model import system_models_repository as system_models_repository
    return system_models_repository


class InMemoryDiagramSearchTest(unittest.TestCase):

    def setUp(self):
        global system_models_repository
        system_models_repository = reload_system_model_repository()
        importlib.reload(diagram_search)

    def test_search_tables_and_users(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user1", nodes.database_user)
        input_model.add_system_node("user2", nodes.database_user)
        input_model.add_system_node("table1", nodes.table)
        input_model.add_system_node("table2", nodes.table)
        input_model.add_system_node("table3", nodes.table)
        input_model.add_system_node("table4", nodes.table)
        # data_model().add_vertex("col1", "column")
        # data_model().add_vertex("col2", "column")
        # data_model().add_vertex("col3", "column")
        input_model.add_relation("user1", "table1", DatamodelRelationTypes.contains)
        input_model.add_relation("user1", "table2", DatamodelRelationTypes.uses)
        input_model.add_relation("user2", "table2", DatamodelRelationTypes.contains)
        input_model.add_relation("user2", "table3", DatamodelRelationTypes.contains)
        input_model.add_relation("user2", "table4", DatamodelRelationTypes.contains)
        # data_model().add_edge("table1","col1",DatamodelRelationTypes.contains)
        # data_model().add_edge("table2","col2",DatamodelRelationTypes.contains)
        # data_model().add_edge("table3","col3",DatamodelRelationTypes.contains)
        system_models_repository.append_system_model(input_model)

        # when
        result = diagram_search.search_database_user("user1")

        # then
        expected = data_model()
        expected.add_system_node("user1", nodes.database_user)
        expected.add_system_node("user2", nodes.database_user)
        expected.add_system_node("table1", nodes.table)
        expected.add_system_node("table2", nodes.table)
        expected.add_relation("user1", "table1", DatamodelRelationTypes.contains)
        expected.add_relation("user1", "table2", DatamodelRelationTypes.uses)
        expected.add_relation("user2", "table2", DatamodelRelationTypes.contains)
        self.assert_models_are_equal(expected, result)

    def test_search_tables_with_columns_and_fk_and_users(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user1", nodes.database_user)
        input_model.add_system_node("user2", nodes.database_user)
        input_model.add_system_node("table1", nodes.table)
        input_model.add_system_node("table2", nodes.table)
        input_model.add_system_node("table3", nodes.table)
        input_model.add_system_node("table4", nodes.table)
        input_model.add_system_node("col1", "column")
        input_model.add_system_node("col2", "column")
        input_model.add_system_node("col3", "column")
        input_model.add_system_node("col4", "column")
        input_model.add_relation("user1", "table1", DatamodelRelationTypes.contains)
        input_model.add_relation("user1", "table2", DatamodelRelationTypes.uses)
        input_model.add_relation("user2", "table2", DatamodelRelationTypes.contains)
        input_model.add_relation("user2", "table3", DatamodelRelationTypes.contains)
        input_model.add_relation("user2", "table4", DatamodelRelationTypes.contains)
        input_model.add_relation("table1", "col1", DatamodelRelationTypes.contains)
        input_model.add_relation("table2", "col2", DatamodelRelationTypes.contains)
        input_model.add_relation("table3", "col3", DatamodelRelationTypes.contains)
        input_model.add_relation("table4", "col4", DatamodelRelationTypes.contains)
        input_model.add_relation("col1", "col3", "fk")
        system_models_repository.append_system_model(input_model)

        # when
        result = diagram_search.search_database_user("user1")

        # then
        expected = data_model()
        expected.add_system_node("user1", nodes.database_user)
        expected.add_system_node("user2", nodes.database_user)
        expected.add_system_node("table1", nodes.table)
        expected.add_system_node("table2", nodes.table)
        expected.add_system_node("table3", nodes.table)
        expected.add_system_node("col1", "column")
        expected.add_system_node("col2", "column")
        expected.add_system_node("col3", "column")
        expected.add_relation("user1", "table1", DatamodelRelationTypes.contains)
        expected.add_relation("user1", "table2", DatamodelRelationTypes.uses)
        expected.add_relation("user2", "table2", DatamodelRelationTypes.contains)
        expected.add_relation("table1", "col1", DatamodelRelationTypes.contains)
        expected.add_relation("table2", "col2", DatamodelRelationTypes.contains)
        expected.add_relation("table3", "col3", DatamodelRelationTypes.contains)
        expected.add_relation("col1", "col3", "fk")
        self.assert_models_are_equal(expected, result)

    def test_search_composition_relation(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user", nodes.database_user)
        input_model.add_system_node(nodes.table, nodes.table)
        input_model.add_system_node("part", nodes.table)
        input_model.add_system_node("parts", "column")
        input_model.add_system_node("column_part", "column")
        input_model.add_relation("user", nodes.table, DatamodelRelationTypes.contains)
        input_model.add_relation("user", "part", DatamodelRelationTypes.contains)
        input_model.add_relation(nodes.table, "parts", DatamodelRelationTypes.contains)
        input_model.add_relation("part", "parts", "composition")
        input_model.add_relation("column_part", "part", DatamodelRelationTypes.contains)
        system_models_repository.append_system_model(input_model)

        # when
        result = diagram_search.search_database_user("user")

        # then
        self.assert_models_are_equal(input_model, result)

    @unittest.skip("because search criteria does not support matching edge&relation combinations")
    def test_search_tables_excluding_not_targeted_users(self):
        # given
        input_model = data_model()
        input_model.add_system_node("user1", nodes.database_user)
        input_model.add_system_node("user2", nodes.database_user)
        input_model.add_system_node("user3", nodes.database_user)
        input_model.add_system_node("table1", nodes.table)
        input_model.add_system_node("col1", "column")
        input_model.add_relation("user1", "table1", DatamodelRelationTypes.uses)
        input_model.add_relation("user2", "table1", DatamodelRelationTypes.contains)
        input_model.add_relation("user3", "table1", DatamodelRelationTypes.uses)
        input_model.add_relation("col1", "table1", DatamodelRelationTypes.contains)

        system_models_repository.append_system_model(input_model)

        # when
        result = diagram_search.search_database_user("user1")

        # then
        expected = data_model()
        expected.add_system_node("user1", nodes.database_user)
        expected.add_system_node("user2", nodes.database_user)
        expected.add_system_node("user3", nodes.database_user)
        expected.add_system_node("col1", "column")
        expected.add_system_node("table1", nodes.table)
        expected.add_relation("user1", "table1", DatamodelRelationTypes.uses)
        expected.add_relation("user2", "table1", DatamodelRelationTypes.contains)
        expected.add_relation("col1", "table1", DatamodelRelationTypes.contains)
        self.assert_models_are_equal(expected, result)


    def test_component_search(self):
        #given
        system_model = component_model()
        system_model.add_system_node("P1","product")
        system_model.add_system_node("app1","application")
        system_model.add_system_node("app2","application")
        system_model.add_system_node("app3","application")
        system_model.add_system_node("t1",nodes.table)

        system_model.add_relation("P1","app1",DatamodelRelationTypes.contains)
        system_model.add_relation("P1","app2",DatamodelRelationTypes.contains)
        system_model.add_relation("P1","app3",DatamodelRelationTypes.contains)
        system_model.add_relation("app1","app3","calls")
        system_model.add_relation("P1","t1","owns")
        system_models_repository.append_system_model(system_model)

        #when
        result = diagram_search.search_component_diagram("P1")

        #then
        expected = component_model()
        expected.add_system_node("P1", "product")
        expected.add_system_node("app1", "application")
        expected.add_system_node("app2", "application")
        expected.add_system_node("app3", "application")

        expected.add_relation("P1", "app1", DatamodelRelationTypes.contains)
        expected.add_relation("P1", "app2", DatamodelRelationTypes.contains)
        expected.add_relation("P1", "app3", DatamodelRelationTypes.contains)
        expected.add_relation("app1", "app3", "calls")
        self.assert_models_are_equal(expected, result)

    def assert_models_are_equal(self, model1: data_model, model2: data_model):
        self.assertDictEqual(model1.graph[SYSTEM_NODES], model2.graph[SYSTEM_NODES])
        self.assertSetEqual(set(hash(frozenset(edge.items())) for edge in model1.get_relations()),
                            set(hash(frozenset(edge.items())) for edge in model2.get_relations()))
