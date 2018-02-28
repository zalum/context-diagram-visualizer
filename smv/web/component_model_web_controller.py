from flask import Blueprint
from flask import request

from smv import web_utils
from smv.web_utils import build_response
from smv.core.actions import render_component_diagram

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
        enum: ["image","text"]
        default: "image"
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
    output_format = request.args.get("format")
    render_result = render_component_diagram(component, output_format)
    return build_response(render_result, output_format)