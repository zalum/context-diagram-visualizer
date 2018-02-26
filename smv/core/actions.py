from smv.core.model import system_models_repository
from smv.core.model.system_model import system_model as system_model
import json


def add_system_node(system_node_id, system_node_type):
    return system_models_repository.add_system_node(system_node_id, system_node_type=system_node_type)


def append_json(json_content):
    graph = json.loads(json_content)
    model = system_model(graph)
    system_models_repository.append_system_model(model)
