import smv.core.model.system_model as sm
from smv.core.model.system_model import DatamodelNodeTypes
from smv.core.model.system_models_repository import SearchCriteria
from smv.core.model import system_models_repository
from smv.core.model.application_config import NEO4J_DB, FILE_SYSTEM_DB, PERSISTANCE_ENGINE
from smv.core.model.application_config import config


def search_database_user(user):
    criteria = get_query(SEARCH_DATABASE_USER).get_native_query(config[PERSISTANCE_ENGINE])
    system_model = system_models_repository.search(user, criteria)
    return sm.data_model(system_model.graph)


def search_component_diagram(component):
    criteria = get_query(SEARCH_SOFTWARE_PRODUCT).get_native_query(config[PERSISTANCE_ENGINE])
    system_model = system_models_repository.search(component, criteria)
    return sm.component_model(system_model.graph)


class SearchQuery:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.in_memory_query = None
        self.cypher_query = None

    def with_in_memory_query(self, in_memory_query: SearchCriteria):
        self.in_memory_query = in_memory_query
        return self

    def get_native_query(self, db_engine):
        if db_engine is NEO4J_DB:
            return self.cypher_query
        if db_engine is FILE_SYSTEM_DB:
            return self.in_memory_query

    def with_cyper_query(self, query):
        self.cypher_query = query
        return self


def get_query(name)->SearchQuery:
    for query in queries:
        if name == query.name:
            return query
    return None


def __create_union_cypher_query(template: str, match_clauses: []):
    return "union".join(map(lambda c: template.format(clause=c), match_clauses))


SEARCH_DATABASE_USER = "SEARCH_DATABASE_USER"
SEARCH_SOFTWARE_PRODUCT = "SEARCH_SOFTWARE_PRODUCT"


queries = [
    SearchQuery(SEARCH_DATABASE_USER, "extracts the datamodel related to a database user ").
    with_in_memory_query(
        SearchCriteria().with_include_vertex_types(0, [DatamodelNodeTypes.table]).
        with_include_vertex_types(1, [DatamodelNodeTypes.database_user, DatamodelNodeTypes.column]).
        with_include_relation_types(1, ["contains"]).
        with_include_relation_types(2, ["fk", "composition"]).
        with_include_vertex_types(3, ["table"]).
        with_max_levels(4)).
    with_cyper_query(
        __create_union_cypher_query("""
MATCH 
p = {clause}
with relationships(p) as rels
unwind rels as rel
return startNode(rel) as start,endNode(rel) as end, type(rel) as relation_type 
       """, [
            "(x:database_user {{system_node_id:'{start_node}'}})-[:uses]-(y:table)-[:contains]-(z:database_user)",
            """
            (x:database_user {{system_node_id:'{start_node}'}})--(y:table)
            -[:contains]-(:column)-[:fk|composition]-(:column)--(:table)-[:uses]-(x:database_user {{system_node_id:'{start_node}'}})
            """,
            """
            (x:database_user {{system_node_id:'{start_node}'}})--(y:table)
            -[:contains]-(:column)
            """
        ]
    )
    ),

    SearchQuery(SEARCH_SOFTWARE_PRODUCT, "extracts the contents of a C4 diagram of a Software product").
    with_in_memory_query(
        SearchCriteria().
        with_include_vertex_types(0, ["application"]).
        with_include_relation_types(0, ["contains"]).
        with_include_vertex_types(1, ["application"]).
        with_include_relation_types(1, ["calls"]).
        with_max_levels(2))
]



