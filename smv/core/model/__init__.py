from smv.core.infrastructure.file_system_model_repository import FileSystemModelsRepository
from smv.core.infrastructure.neo4j_system_model_repository import Neo4JSystemModelsRepository
from smv.core.model.application_config import config
from smv.core.model.system_models_repository import SystemModelsRepository


system_models_repository = None  # type: SystemModelsRepository


def get_system_model_repository()->SystemModelsRepository:
    if config["persistance-engine"] is "neo4j":
        return Neo4JSystemModelsRepository()
    else:
        return FileSystemModelsRepository()


def load_context():
    global system_models_repository
    system_models_repository = get_system_model_repository()


load_context()
