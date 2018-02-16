from smv.core.model import system_models_repository


def add_system_node(system_node_id, system_node_type):
    return system_models_repository.add_system_node(system_node_id, system_node_type=system_node_type)
