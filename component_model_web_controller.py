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
                          rule_filter=lambda rule: web_utils.rule_filter(rule,['/component','/relation'])
                          ),
    url_prefix="/component-model")


@config.controller.route("/component", methods=['POST'])
def add_component():
    '''
    create component
    ---
    parameters:
      - in: body
        name: component
        required: true
        schema:
            type: string
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

@config.controller.route("/relation", methods=['POST'])
def create_relation():
    '''
    create relation
    ---
    parameters:
          - in: body
            name: relation
            required: true
            schema:
                type: object
                properties:
                    start:
                        type: string
                    end:
                        type: string
                    relation_type:
                        type: string
                        enum: ["contains","calls"]
                examples:
                    example:
                        start: app1
                        end: app2
                        relation_type: contains
    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - component
    '''
    relation = request.get_json()
    system_model.state.add_edge(start=relation["start"],end=relation["end"],relation_type=relation["relation_type"])
    return "ok"

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
    return json.dumps(system_model.state.find_connected_graph(component).graph)

@config.controller.route("/component/<string:component>/diagram",methods=['GET'])
def draw_component_diagram(component):
    pass

