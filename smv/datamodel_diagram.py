import smv.core.model.system_model as sm
from smv.search_model import search_criteria, find_connected_graph
from smv.core.model import system_models_repository


def search_database_user(user):
    state = system_models_repository.get_full_system_model()
    criteria = search_criteria().with_include_vertex_types(0, ["table"]). \
        with_include_vertex_types(1, ["database-user", "column"]). \
        with_include_relation_types(1, ["contains"]). \
        with_include_relation_types(2, ["fk", "composition"]). \
        with_include_vertex_types(3, ["table"])

    return sm.data_model(find_connected_graph(state, user, level=4, criteria=criteria).graph)
