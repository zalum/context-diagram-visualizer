from smv.core.model import system_model
from smv.search_model import search_criteria, find_connected_graph
from smv.system_model_state import state


def search(component):
    criteria = search_criteria().with_include_vertex_types(0,["application"])
    return system_model.component_model(find_connected_graph(state, component, criteria=criteria, level=1).graph)