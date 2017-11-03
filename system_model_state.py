
import logging
import system_model
import os
import json
from json import JSONDecodeError

def read_state():
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

