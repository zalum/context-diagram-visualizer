from neo4j.v1 import GraphDatabase, basic_auth, session

from smv.core.model import system_model
from smv.core.model.system_models_repository import SystemModelsRepository


def __get_db_session()->session:
    global driver
    if driver is None:
        driver = GraphDatabase.driver('bolt://localhost', auth=basic_auth("neo4j", "xxx"))
    return driver.session()


class Neo4JSystemModelsRepository(SystemModelsRepository):

    def find_connected_graph(self, system_mode, level=None) -> system_model:
        pass

    def add_vertex(self, system_node_id, system_node_type):
        pass

    def get_full_system_model(self) -> system_model:
        pass

    def append_system_model(self, system_model):
        pass

    def search(self, system_mode, criteria: 'SearchCriteria', level) -> system_model:
        pass

    def set_model(self, system_mode):
        pass
