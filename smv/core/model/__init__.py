from smv.core.infrastructure.neo4j_system_model_repository import Neo4JSystemModelsRepository
from smv.core.model.system_models_repository import SystemModelsRepository


def get_system_model_repository()->SystemModelsRepository:
    return Neo4JSystemModelsRepository()


system_models_repository = get_system_model_repository()
