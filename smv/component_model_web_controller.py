import json

from flask import Blueprint
from flask import abort
from flask import request

from smv import web_utils, system_model
from smv.system_model_state import state
from smv.system_model_visualizer import component_model_visualizer as cmv
from smv.web_utils import build_diagram_response

config = web_utils.web_controller_config(
    controller = Blueprint('component-model', 'component-model'),
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
    state.add_vertex(component["name"],type=component["type"])
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
    component_type = request.args.get("type")
    if component_type is None:
        return abort(400,"Type cannot be null")

    return json.dumps([key for key in state.get_vertexes_of_type(component_type)])


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
    result = state.add_edge(start=relation["start"], end=relation["end"], relation_type=relation["relation_type"])
    if result is system_model.RESPONSE_OK:
        return "ok"
    else:
        abort(400,result)

@config.controller.route("/component/<string:component>/direct-connections",methods=['GET'])
def get_direct_connections(component):
    '''
    get direct connections of component
    ---
    parameters:
        - in: path
          type: string
          name: component
          required: true
        - in: query
          type: string
          name: type
          required: false
          enum: ["db-user","application","product"]
        - in: query
          name: relation-type
          required: false
          type: string
          enum: ["contains","calls","uses"]
    responses:
            200:
                content:
                    text/plain:
                      schema:
                        type: string
    tags:
     - component
    '''
    vertex = state.get_vertex(component)
    type = request.args.get("type")
    relation_type = request.args.get("relation-type")
    if vertex is None:
        abort(404)
    connections = state.find_direct_connections(component,type,relation_type)
    return json.dumps(connections)


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
    return json.dumps(state.get_vertex(component))

@config.controller.route("/component/<string:component>/graph",methods=['GET'])
def get_component_graph(component):
    '''
    get component graph
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
    return json.dumps(state.find_connected_graph(component))


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
    component_model = system_model.component_model(state.find_connected_graph(component))
    diagram = cmv(component_model).draw()
    return build_diagram_response(diagram, "image")