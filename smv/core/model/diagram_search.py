import smv.core.model.system_model as sm
from smv.core.model.system_models_repository import SearchCriteria
from smv.core.model import system_models_repository


def search_database_user(user):
    criteria = SearchCriteria().with_include_vertex_types(0, ["table"]). \
        with_include_vertex_types(1, ["database-user", "column"]). \
        with_include_relation_types(1, ["contains"]). \
        with_include_relation_types(2, ["fk", "composition"]). \
        with_include_vertex_types(3, ["table"])

    system_model = system_models_repository.search(user, criteria, level=4)
    return sm.data_model(system_model.graph)


def search_component_diagram(component):
    criteria = SearchCriteria().with_include_vertex_types(0, ["application"])
    system_model = system_models_repository.search(component, criteria, level=1)
    return sm.component_model(system_model.graph)
