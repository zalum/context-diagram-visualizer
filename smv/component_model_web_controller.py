from flask import Blueprint
from flask import request


from smv import web_utils, system_model
from smv.system_model_state import state
from smv.system_model_visualizer import component_model_visualizer as cmv
from smv.web_utils import build_diagram_response

config = web_utils.web_controller_config(
    controller = Blueprint('component-model', 'component-model'),
    url_prefix="/component-model")

@config.controller.route("/component/<string:component>/diagram",methods=['GET'])
def draw_component_diagram(component):
    '''
    get diagram
    ---
    parameters:
      - in: path
        type: string
        name: component
        required: true
      - in: query
        type: string
        name: format
        enum: ["image","plantuml.md"]
        default: ["image"]
        required: true
    responses:
        200:
            content:
                image/png:
                  schema:
                    type: file
                    format: binary
    tags:
    - component
    '''
    component_model = system_model.component_model(state.find_connected_graph(component).graph)
    diagram = cmv(component_model).draw()
    return build_diagram_response(diagram, request.args.get("format"))