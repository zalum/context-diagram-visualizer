from neo4j.v1 import GraphDatabase, session

from smv.core.model.system_model import system_model
from smv.core.model.system_model import DatamodelNodeTypes
from smv.core.model.system_models_repository import SystemModelsRepository, SearchCriteria
from smv.core.common import Response

driver = None


def get_db_session() -> session:
    global driver
    if driver is None:
        driver = GraphDatabase.driver('bolt://localhost')
    return driver.session()


class Neo4JSystemModelsRepository(SystemModelsRepository):
    def add_relation(self, start, end, relation_type):
        with get_db_session() as session:
            session.write_transaction(self.__write_relation, start, end, relation_type)
        return Response.success()

    def find_connected_graph(self, system_mode, level=None) -> system_model:
        pass

    def add_vertex(self, name, type):
        with get_db_session() as session:
            session.write_transaction(self.__write_system_node, name, type)
        return Response.success(name)

    def get_full_system_model(self) -> system_model:
        pass

    def append_system_model(self, sm: system_model):
        with get_db_session() as session:
            session.write_transaction(self.__write_system_nodes, sm)
            session.write_transaction(self.__write_relations, sm)

    @staticmethod
    def __write_system_nodes(tx, sm: system_model):
        for system_node in sm.get_system_nodes():
            system_node_properties = sm.get_system_node(system_node)
            Neo4JSystemModelsRepository.__write_system_node(tx, system_node, system_node_properties["type"])

    @staticmethod
    def __write_system_node(tx, name, type):
        tx.run("CREATE (node:`{}`".format(type) + " {name: $name})",
               name=name)

    @staticmethod
    def __write_relations(tx, sm: system_model):
        for relation in sm.get_relations():
            Neo4JSystemModelsRepository.__write_relation(tx, **relation)

    def get_node(self, node):
        with get_db_session() as session:
            result = session.read_transaction(self.__get_node, node)
        return result

    @staticmethod
    def __get_node(tx, node):
        result = tx.run("match (x {name:$name}) return x", name=node)
        record = result.single()
        if record is None:
            return None
        return record[0].get("name")

    @staticmethod
    def __write_relation(tx, start, end, relation_type=None):
        if relation_type is not None:
            merge_query = "merge  (x)-[:{}]-(y)".format(relation_type)
        else:
            merge_query = "merge  (x)-[:unknown]-(y)"
        match_query = """match 
            (x {name: $start_name}),
            (y {name: $end_name})"""
        tx.run(
            "{} {}".format(match_query, merge_query)
            , start_name=start, end_name=end
        )

    def search(self, system_mode, criteria: SearchCriteria, level) -> system_model:
        pass

    def set_model(self, system_mode):
        pass
