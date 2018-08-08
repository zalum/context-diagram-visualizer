from smv.core import Response
from smv.core.model import system_model


class SystemModelsRepository(object):

    def add_vertex(self,system_node_id, system_node_type):
        pass

    def add_relation(self,start, end, relation_type)->Response:
        pass

    def get_full_system_model(self)-> system_model:
        pass

    def search(self, system_mode, criteria: 'SearchCriteria', level)->system_model:
        pass

    def find_connected_graph(self, system_mode, level)->Response:
        pass

    def set_model(self, system_mode):
        pass

    def append_system_model(self,system_model):
        pass

    def get_node(self, node):
        pass


class SearchCriteria:
    def __init__(self):
        self.levels_criteria = dict()

    def level_search_criteria(self,level):
        if level not in self.levels_criteria:
            self.levels_criteria[level] = {"include_vertex_types": [], "include_relation_types":[]}
        return self.levels_criteria[level]

    def with_include_vertex_types(self, level, vertex_types:[])-> 'SearchCriteria':
        level_search_criteria = self.level_search_criteria(level)
        for vertex_type in vertex_types:
            level_search_criteria["include_vertex_types"].append(vertex_type)
        return self

    def include_vertex_types(self,level):
        return self.level_search_criteria(level)["include_vertex_types"]

    def has_criteria(self, level):
        if level in self.levels_criteria:
            return True
        return False

    def with_include_relation_types(self, level, relation_types)-> 'SearchCriteria':
        level_search_criteria = self.level_search_criteria(level)
        for relation_type in relation_types:
            level_search_criteria["include_relation_types"].append(relation_type)
        return self

    def include_relation_types(self,level)->[]:
        return self.level_search_criteria(level)["include_relation_types"]



