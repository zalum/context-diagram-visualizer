from  smv.system_model import system_model

class search_criteria():
    def __init__(self):
        self.levels_criteria = dict()

    def level_search_criteria(self,level):
        if level not in self.levels_criteria:
            self.levels_criteria[level] = {"include_vertex_types": [], "include_relation_types":[]}
        return self.levels_criteria[level]

    def with_include_vertex_types(self, level, vertex_types:[])->'search_criteria':
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

    def with_include_relation_types(self, level, relation_types)->'search_criteria':
        level_search_criteria = self.level_search_criteria(level)
        for relation_type in relation_types:
            level_search_criteria["include_relation_types"].append(relation_type)
        return self

    def include_relation_types(self,level)->[]:
        return self.level_search_criteria(level)["include_relation_types"]


def matching_edge(criteria:search_criteria, model:system_model, current_level, edge):
    if criteria is None:
        return True
    if criteria.has_criteria(current_level) is False:
        return True

    include_vertex_types = criteria.include_vertex_types(current_level)
    if len(include_vertex_types) is not 0:
        vertex_types = [model.get_vertex(edge["start"])["type"], model.get_vertex(edge["end"])["type"]]
        for vertex_types_to_match in include_vertex_types:
            if vertex_types_to_match in vertex_types:
                return True
        return False

    include_relation_types = criteria.include_relation_types(current_level)
    if len(include_relation_types) is not 0:
        for accepted_relation_type in include_relation_types:
            if "relation_type" in edge and accepted_relation_type == edge["relation_type"]:
                return True
        return False
    return True


def find_connected_graph(source_model: system_model, from_vertex, criteria = None, level=None, connected_model=None, current_level=0):
    if connected_model is None:
        connected_model = system_model()
        if not source_model.has_vertex(from_vertex):
            return connected_model
        connected_model.copy_vertex(source_model, from_vertex)

    if level is not None and current_level == level:
        return connected_model

    adjacent_vertexes = set()
    for edge in source_model.get_edges_of_vertex(from_vertex):
        if matching_edge(criteria, source_model, current_level, edge) is False:
            continue
        adjacent_vertex = source_model.get_related_vertex(vertex=from_vertex, edge=edge)
        if adjacent_vertex not in source_model.graph["vertexes"]:
            continue
        if connected_model.get_vertex(adjacent_vertex) is None:
            connected_model.copy_vertex(source_model, adjacent_vertex)
            adjacent_vertexes.add(adjacent_vertex)
        connected_model.add_edge(**edge)

    for adjacent_vertex in adjacent_vertexes:
        connected_model = find_connected_graph(source_model,
                                                            from_vertex=adjacent_vertex,
                                                            criteria=criteria,
                                                            level=level,
                                                            connected_model=connected_model,
                                                            current_level=current_level+1)

    return connected_model