from smv.search_model import search_criteria, find_connected_graph
import smv.system_model as sm
from smv.system_model_state import state


def search_database_user(user):
    criteria = search_criteria().with_include_vertex_types(0, ["table"]). \
        with_include_vertex_types(1, ["database-user", "column"]). \
        with_include_relation_types(1, ["contains"]). \
        with_include_relation_types(2, ["fk"]). \
        with_include_vertex_types(3, ["table"])

    return sm.data_model(find_connected_graph(state, user, level=4, criteria=criteria).graph)