from flask import request
from flask import Blueprint
from smv.web_utils import build_diagram_response
from smv.web_utils import web_controller_config

config = web_controller_config(
    controller = Blueprint('plantuml', 'plantuml'),
    url_prefix="/plantuml")


@config.controller.route("/diagram", methods=['POST'])
def draw_plant_uml():
    '''
    generate a diagram from plantuml mark-down
    ---
    parameters:
      - in: body
        name: plantuml
        required: true
        schema:
            type: string
    responses:
        200:
            content:
                image/png:
                  schema:
                    type: file
                    format: binary
    tags:
    - plantuml
    '''
    return build_diagram_response(request.data,output_format="image",input_format="block")