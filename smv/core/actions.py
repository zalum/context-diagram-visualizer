from smv.system_model_state import state


def add_system_node(id,type):
    state.add_vertex(id, type=type)
