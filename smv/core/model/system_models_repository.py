from smv.core import Response
from smv.core.model import system_model


class SystemModelsRepository(object):

    def add_vertex(self,system_node_id, system_node_type, name=None):
        pass

    def add_relation(self,start, end, relation_type)->Response:
        pass

    def get_full_system_model(self)-> system_model:
        pass

    def search(self, start_node, search_query) ->system_model:
        pass

    def find_connected_graph(self, system_node, level)->Response:
        pass

    def filter(self, node_type):
        pass

    def append_system_model(self, system_model):
        pass

    def get_node(self, node):
        pass


class SearchCriteria:
    def __init__(self):
        self.levels_criteria = dict()
        self.max_levels = None

    def __init_level_search_criteria(self, level):
        if level not in self.levels_criteria:
            self.levels_criteria[level] = {"include_vertex_types": [], "include_relation_types":[]}
        return self.levels_criteria[level]

    def with_include_vertex_types(self, level, vertex_types:[])-> 'SearchCriteria':
        level_search_criteria = self.__init_level_search_criteria(level)
        for vertex_type in vertex_types:
            level_search_criteria["include_vertex_types"].append(vertex_type)
        return self

    def with_max_levels(self, max_levels):
        self.max_levels = max_levels
        return self

    def has_criteria(self, level):
        if level in self.levels_criteria:
            return True
        return False

    def with_include_relation_types(self, level, relation_types)-> 'SearchCriteria':
        level_search_criteria = self.__init_level_search_criteria(level)
        for relation_type in relation_types:
            level_search_criteria["include_relation_types"].append(relation_type)
        return self

    def get_include_vertex_types(self, level):
        return self.__init_level_search_criteria(level)["include_vertex_types"]

    def get_include_relation_types(self, level)->[]:
        return self.__init_level_search_criteria(level)["include_relation_types"]



