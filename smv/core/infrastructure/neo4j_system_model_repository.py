from typing import Tuple

from neo4j.v1 import GraphDatabase, Session, Record, Node, BoltStatementResult

from smv.core.model.system_model import system_model
from smv.core.model.system_models_repository import SystemModelsRepository
from smv.core.common import Response
from smv.core.model.application_config import config
from smv.core.model.application_config import NEO4J_URL
import logging

neo4j_log = logging.getLogger("neo4j.bolt")
neo4j_log.setLevel(logging.WARNING)

driver = None


def __is_connection_encrypted():
    open_ssl_1_0_1_bug_on_system = True
    return not open_ssl_1_0_1_bug_on_system


def get_db_session() -> Session:
    global driver
    if driver is None:
            driver = GraphDatabase.driver(config[NEO4J_URL], encrypted=__is_connection_encrypted())
    return driver.session()


def query_db(query, **params) -> BoltStatementResult:
    with get_db_session() as db_session:
        return db_session.read_transaction(lambda tx: tx.run(query, **params))



def write_db(query: Tuple[str, dict]) -> BoltStatementResult:
    with get_db_session() as db_session:
        return db_session.write_transaction(lambda tx: tx.run(query[0], **query[1]))


def write_bulk_db(queries: [Tuple[str, dict]]):
    with get_db_session() as db_session:
        for query in queries:  # type: tuple
            db_session.write_transaction(lambda tx: tx.run(query[0], **query[1]))


class Neo4jSearchCriteria:
    __union_template = """
MATCH 
p = {clause}
with relationships(p) as rels
unwind rels as rel
return startNode(rel) as start,endNode(rel) as end, type(rel) as relation_type 
    """

    def __init__(self, match_clauses):
        self.match_clauses = match_clauses

    def generate_query(self, **params):
        query = self.__create_union_query(match_clauses=self.match_clauses)
        return query.format(**params)

    @staticmethod
    def __create_union_query(match_clauses: []):
        return "union".join(map(lambda c: Neo4jSearchCriteria.__union_template.format(clause=c), match_clauses))


class Neo4JSystemModelsRepository(SystemModelsRepository):

    def filter(self, node_type):
        query_result = query_db("match (x:{node_type}) return x".format(node_type=node_type))
        result = {}
        for record in query_result.records():
            node = Neo4JSystemModelsRepository.__extract_system_node(record[0])
            result.update({node["system_node_id"]: node["properties"]})
        return result

    def get_node(self, node):
        result = query_db("match (x {system_node_id:$system_node_id}) return x", system_node_id=node)
        record = result.single()
        if record is None:
            return None
        return record[0].get("system_node_id")

    def add_vertex(self, system_node_id, node_type, name=None):
        write_db(self.__add_system_node_query(system_node_id, node_type, name))
        return Response.success(system_node_id)

    def add_relation(self, start, end, relation_type):
        response = write_db(self.__add_relation_query(start, end, relation_type))
        return Response.success(response.summary())

    def find_connected_graph(self, system_node, level) -> system_model:
        if level is None:
            return Response.error("Neo4j find_connected_graph implementation does work on unlimited levels")

        if level <= 0:
            return Response.error("The level to search should be greater then 0")

        query = """
        MATCH p = 
            (x:database_user {system_node_id:'APP_LNC'})--(:table)-[:contains]-(:database_user),
            (x:database_user {system_node_id:'APP_LNC'})--(:table)-[:contains]-(:column)
        with relationships(p) as rels
        unwind rels as rel
        return startNode(rel) as start,endNode(rel) as end, type(rel) as relation_type
        """.format(system_node, level)
        result = query_db(query)
        return Response.success(self.__extract_model(result))

    def append_system_model(self, sm: system_model):
        self.__write_system_nodes(sm)
        self.__write_relations(sm)

    @staticmethod
    def __extract_model(results: BoltStatementResult):
        model = system_model()
        for record in results.records():  # type: Record
            start = Neo4JSystemModelsRepository.__add_node_to_model(model, record, "start")
            end = Neo4JSystemModelsRepository.__add_node_to_model(model, record, "end")
            model.add_relation(start, end, record.value("relation_type"))
        return model

    @staticmethod
    def __add_node_to_model(model, record, record_key):
        node_value = Neo4JSystemModelsRepository.__extract_system_node(record.value(record_key))
        model.add_system_node(node_value["system_node_id"], node_value["type"], **node_value["properties"])
        return node_value["system_node_id"]

    @staticmethod
    def __extract_system_node(node: Node):
        result = dict()
        result["system_node_id"] = node.get("system_node_id")
        if len(node.labels) > 0:
            result["type"] = list(node.labels).pop()
        properties = dict()
        properties.update(filter(lambda x: x[0] != "system_node_id", node.items()))
        result["properties"] = properties
        return result

    @staticmethod
    def __add_relation_query(start, end, relation_type):
        if relation_type is not None:
            merge_query = "merge  (x)-[:{}]-(y)".format(relation_type)
        else:
            merge_query = "merge  (x)-[:unknown]-(y)"
        match_query = """match 
                   (x {system_node_id: $start}),
                   (y {system_node_id: $end})"""

        return "{} {}".format(match_query, merge_query), dict(start=start, end=end)

    @staticmethod
    def __add_system_node_query(system_node_id, node_type, name):
        query = "MERGE (node:{} ".format(node_type)
        query += " {system_node_id: $system_node_id})"
        arguments = {"system_node_id": system_node_id}
        if name is not None:
            query += "ON CREATE SET node.name = $name"
            arguments["name"] = name
        return query, arguments

    @staticmethod
    def __write_system_nodes(sm: system_model):
        queries = []
        for system_node in sm.get_system_nodes():
            system_node_properties = sm.get_system_node(system_node)
            query = Neo4JSystemModelsRepository.__add_system_node_query(system_node,
                                                                        system_node_properties.get("type"),
                                                                        system_node_properties.get("name"))
            queries.append(query)

        write_bulk_db(queries)

    @staticmethod
    def __write_relations( sm: system_model):
        queries = []
        for relation in sm.get_relations():
            query = Neo4JSystemModelsRepository.__add_relation_query(**relation)
            queries.append(query)
        write_bulk_db(queries)

    def search(self, start_node, search_query: Neo4jSearchCriteria) -> system_model:
        query = search_query.generate_query(start_node=start_node)
        result = query_db(query)
        return self.__extract_model(result)

    def get_full_system_model(self) -> system_model:
        query = """
        MATCH p = (x)--(y) with relationships(p) as rels 
        unwind rels as rel 
        return startNode(rel) as start,endNode(rel) as end, type(rel) as relation_type
        """
        result = query_db(query)
        return self.__extract_model(result)
