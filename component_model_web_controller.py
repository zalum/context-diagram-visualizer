from flask import Blueprint
import system_model
import web_utils
import json
from flask import abort
from flask import request


config = web_utils.web_controller_config(
    controller = Blueprint('component-model', 'component-model'),
    swagger_config = dict(endpoint = "component-model",
                          route = "/component-model.json",
                          rule_filter=lambda rule: web_utils.rule_filter(rule,['/component'])
                          ),
    url_prefix="/component-model")

@config.controller.route("/component", methods=['POST'])
def add_component():
    '''
    create component
    ---
    parameters:
      - in: body
        required: true
        schema:
            type: object
            properties:
                name:
                    type: string
                type:
                    type: string
                    enum: ["application","product"]
            examples:
                example:
                    name: productXYZ
                    type: product
    responses:
        200:
            content:
            text/plain:
              schema:
                type: string
    tags:
    - component
    '''
    component = request.get_json()
    system_model.state.add_vertex(component["name"],type=component["type"])
    return "ok"

@config.controller.route("/component", methods=['GET'])
def list_components():
    '''
    list component
    ---
    parameters:
          - in: query
            type: string
            name: type
            required: true
            enum: ["application","product"]
    responses:
        200:
            content:
            text/plain:
              schema:
                type: string
    tags:
    - component
    '''
    type = request.args.get("type")
    if type is None:
        return abort(400,"Type cannot be null")

    return json.dumps([key for key in system_model.state.get_vertexes_of_type(type)])


@config.controller.route("/component/<string:component>",methods=['GET'])
def get_component(component):
    '''
    get component
    ---
    parameters:
      - in: path
        type: string
        name: component
        required: true
    responses:
        200:
            content:
            text/plain:
              schema:
                type: string
    tags:
    - component
    '''
    return json.dumps(component)

