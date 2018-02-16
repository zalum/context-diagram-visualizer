import json
import logging
import os
from json import JSONDecodeError

from smv.core.model.system_models_repository import SystemModelsRepository
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
    def __init__(self):
        self.state = _read_state()

    def get_full_system_model(self)-> system_model:
        return self.state

    def add_vertex(self, system_node_id, system_node_type):
        return self.state.add_vertex(system_node_id,system_node_type)
