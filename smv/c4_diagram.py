from smv.core.model import system_model
from smv.search_model import search_criteria, find_connected_graph
from smv.core.model import system_models_repository


def search(component):
    state = system_models_repository.get_full_system_model()
    criteria = search_criteria().with_include_vertex_types(0,["application"])
    return system_model.component_model(find_connected_graph(state, component, criteria=criteria, level=1).graph)