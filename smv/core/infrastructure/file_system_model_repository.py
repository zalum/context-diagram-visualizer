import json
import logging
import os
from json import JSONDecodeError

from smv.core import Response
from smv.core.model.system_models_repository import SystemModelsRepository, SearchCriteria
from smv.core.model.system_model import system_model


def _read_state() -> system_model:
    file_name = "graph.json"
    if os.path.isfile(file_name) is False:
        return system_model()
    else:
        f = open(file_name, 'r')

        lines = " ".join(f.readlines())
        try:
            graph = json.loads(lines)
        except JSONDecodeError as error:
            logging.warning("File {} can not be converted to json because '{}'".format(file_name, error))
            return system_model()
        return system_model(graph)


class FileSystemModelsRepository(SystemModelsRepository):
    def filter(self, node_type):
        result = {}
        for node in self.state.get_system_nodes_of_type(node_type):
            result[node] = self.state.get_system_node(node)
        return result

    def get_node(self, node):
        self.state.get_system_node(node)

    def add_relation(self, start, end, relation_type=None):
        self.state.add_relation(start, end, relation_type)
        return Response.success()

    def find_connected_graph(self, system_node, level=None) -> Response:
        return Response.success(_find_connected_graph(self.state, system_node,
                                                      criteria=SearchCriteria().with_max_levels(level)))

    def search(self, start_node, search_query: SearchCriteria) -> system_model:
        return _find_connected_graph(self.state, start_node, search_query)

    def __init__(self):
        self.state = _read_state()

    def append_system_model(self, model: system_model):
        self.state.append(model)

    def get_full_system_model(self) -> system_model:
        return self.state

    def add_vertex(self, system_node_id, system_node_type, name=None):
        return self.state.add_system_node(system_node_id, system_node_type, name=name)


def _matching_edge(criteria: SearchCriteria, model: system_model, current_level, edge):
    if criteria is None:
        return True
    if criteria.has_criteria(current_level) is False:
        return True

    include_vertex_types = criteria.get_include_vertex_types(current_level)
    if len(include_vertex_types) != 0:
        vertex_types = [model.get_system_node(edge["start"])["type"], model.get_system_node(edge["end"])["type"]]
        for vertex_types_to_match in include_vertex_types:
            if vertex_types_to_match in vertex_types:
                return True
        return False

    include_relation_types = criteria.get_include_relation_types(current_level)
    if len(include_relation_types) != 0:
        for accepted_relation_type in include_relation_types:
            if "relation_type" in edge and accepted_relation_type == edge["relation_type"]:
                return True
        return False
    return True


def _find_connected_graph(source_model: system_model, from_vertex, criteria: SearchCriteria=None, connected_model=None,
                          current_level=0):
    if connected_model is None:
        connected_model = system_model()
        if not source_model.has_system_node(from_vertex):
            return connected_model
        connected_model.copy_system_node(source_model, from_vertex)

    if criteria.max_levels is not None and current_level == criteria.max_levels:
        return connected_model

    adjacent_vertexes = set()
    for edge in source_model.get_relations_of_system_node(from_vertex):
        if _matching_edge(criteria, source_model, current_level, edge) is False:
            continue
        adjacent_vertex = source_model.get_related_system_node(system_node=from_vertex, edge=edge)
        if source_model.has_system_node(adjacent_vertex) is False:
            continue
        if connected_model.get_system_node(adjacent_vertex) is None:
            connected_model.copy_system_node(source_model, adjacent_vertex)
            adjacent_vertexes.add(adjacent_vertex)
        connected_model.add_relation(**edge)

    for adjacent_vertex in adjacent_vertexes:
        connected_model = _find_connected_graph(source_model,
                                                from_vertex=adjacent_vertex,
                                                criteria=criteria,
                                                connected_model=connected_model,
                                                current_level=current_level + 1)

    return connected_model
