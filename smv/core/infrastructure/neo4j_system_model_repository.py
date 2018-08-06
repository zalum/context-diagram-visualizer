from neo4j.util import watch
from neo4j.v1 import GraphDatabase, session, Transaction

from smv.core.model.system_model import system_model
from smv.core.model.system_models_repository import SystemModelsRepository, SearchCriteria
from smv.core.common import Response
import logging
neo4j_log = logging.getLogger("neo4j.bolt")
neo4j_log.setLevel(logging.WARNING)

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

    def add_vertex(self, node_id, type):
        with get_db_session() as session:
            session.write_transaction(self.__write_system_node, node_id, type)
        return Response.success(node_id)

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
            Neo4JSystemModelsRepository.__write_system_node(tx, system_node,
                                                            system_node_properties.get("type"),
                                                            system_node_properties.get("name"))

    @staticmethod
    def __write_system_node(tx, system_node_id, node_type, name=None):
        query = "MERGE (node:{} ".format(node_type)
        query += " {system_node_id: $system_node_id})"
        arguments = {"system_node_id": system_node_id}
        if name is not None:
            query += "ON CREATE SET node.name = $ name"
            arguments["name"] = name
        tx.run(query, arguments)

    @staticmethod
    def __write_relations(tx, sm: system_model):
        for relation in sm.get_relations():
            Neo4JSystemModelsRepository.__write_relation(tx, **relation)

    def get_node(self, node):
        with get_db_session() as session:
            result = session.read_transaction(self.__get_node, node)
        return result

    @staticmethod
    def __get_node(tx:Transaction, node):
        result = tx.run("match (x {system_node_id:$system_node_id}) return x", system_node_id=node)
        record = result.single()
        if record is None:
            return None
        return record[0].get("system_node_id")

    @staticmethod
    def __write_relation(tx:Transaction, start, end, relation_type=None):
        if relation_type is not None:
            merge_query = "merge  (x)-[:{}]-(y)".format(relation_type)
        else:
            merge_query = "merge  (x)-[:unknown]-(y)"
        match_query = """match 
            (x {system_node_id: $start}),
            (y {system_node_id: $end})"""
        result = tx.run(
            "{} {}".format(match_query, merge_query)
            , start=start, end=end
        )
        return Response.success(result.summary())

    def search(self, system_mode, criteria: SearchCriteria, level) -> system_model:
        pass

    def set_model(self, system_mode):
        pass
