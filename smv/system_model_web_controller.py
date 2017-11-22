import json

from flask import Blueprint

from smv import web_utils
from smv.system_model_state import state

config = web_utils.web_controller_config(
    controller=Blueprint('system-model', 'system-model'),
    url_prefix="/system-model"
)


@config.controller.route("/state/", methods=['PUT'])
def persist_state():
    """
    persist the state to the disc
    ---
    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - system
    """
    f = open("graph.json", 'w')
    content = json.dumps(state.graph)
    f.write(content)
    f.close()
    return "ok"
