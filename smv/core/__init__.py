from smv.core.common import *
from smv.core.infrastructure.file_system_model_repository import FileSystemModelsRepository
from smv.core.infrastructure.neo4j_system_model_repository import Neo4JSystemModelsRepository

NEO4J_DB = "NEO4J_DB"
FILE_SYSTEM_DB = "FILE_SYSTEM_DB"


def get_config(var):
    config = dict(db_option=FILE_SYSTEM_DB)
    return config[var]


def init_infrastructure():
    global system_models_repository
    db_option = get_config("db_option")
    if db_option == NEO4J_DB:
        system_models_repository = FileSystemModelsRepository()
    else:
        if db_option == FILE_SYSTEM_DB:
            system_models_repository = Neo4JSystemModelsRepository()


# init_infrastructure()

