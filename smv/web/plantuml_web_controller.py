from flask import request
from flask import Blueprint
from smv.web_utils import build_response
from smv.web_utils import web_controller_config
from smv.core.actions import render_datamodel_diagram_from_plantuml

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
            description: Ok
            content:
                image/png:
                  schema:
                    type: string
                    format: binary
    tags:
    - plantuml
    '''
    markdown = request.data.decode().split("\n")
    output_format = "image"
    result = render_datamodel_diagram_from_plantuml(markdown,output_format)
    return build_response(result, output_format)