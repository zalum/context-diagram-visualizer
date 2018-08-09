import smv.core.model.system_model as sm
from smv.core.model.system_model import DatamodelNodeTypes
from smv.core.model.system_models_repository import SearchCriteria
from smv.core.model import system_models_repository


def search_database_user(user):
    criteria = SearchCriteria().with_include_vertex_types(0, [DatamodelNodeTypes.table]). \
        with_include_vertex_types(1, [DatamodelNodeTypes.database_user, DatamodelNodeTypes.column]). \
        with_include_relation_types(1, ["contains"]). \
        with_include_relation_types(2, ["fk", "composition"]). \
        with_include_vertex_types(3, ["table"]).\
        with_max_levels(4)

    system_model = system_models_repository.search(user, criteria)
    return sm.data_model(system_model.graph)


def search_component_diagram(component):
    criteria = SearchCriteria().\
        with_include_vertex_types(0, ["application"]).\
        with_include_relation_types(0, ["contains"]).\
        with_include_vertex_types(1, ["application"]).\
        with_include_relation_types(1, ["calls"]).\
        with_max_levels(2)
    system_model = system_models_repository.search(component, criteria)
    return sm.component_model(system_model.graph)
