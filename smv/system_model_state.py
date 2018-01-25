
import json
import logging
import os
from json import JSONDecodeError

from smv.core.model import system_model


def read_state() -> system_model:
    file_name = "graph.json"
    if os.path.isfile(file_name) is False:
        return system_model.system_model()
    else:
        f = open(file_name, 'r')

        lines = " ".join(f.readlines())
        try:
            graph = json.loads(lines)
        except JSONDecodeError as error:
            logging.warning("File {} can not be converted to json because '{}'".format(file_name,error))
            return system_model.system_model()
        return system_model.system_model(graph)


state = read_state()



