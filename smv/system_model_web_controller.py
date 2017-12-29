import json

from flask import Blueprint
from flask import request
from flask import abort

from smv import web_utils
from smv.system_model_state import state
from smv.system_model import RESPONSE_OK

config = web_utils.web_controller_config(
    controller=Blueprint('system-model', 'system-model'),
    url_prefix="/system-model"
)

@config.controller.route("/system-node/<string:node>/graph",methods=['GET'])
def get_node_graph(node):
    '''
    get node graph
    ---
    parameters:
      - in: path
        type: string
        name: node
        required: true
    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - system
    '''
    return json.dumps(state.find_connected_graph(node))

@config.controller.route("/system-node/<string:node>",methods=['GET'])
def get_node(node):
    '''
    get node
    ---
    parameters:
      - in: path
        type: string
        name: node
        required: true
    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - system
    '''
    return json.dumps(state.get_vertex(node))


@config.controller.route("/system-node", methods=['POST'])
def add_system_node():
    '''
    create system node
    ---
    parameters:
      - in: body
        name: node
        required: true
        schema:
            type: string
            properties:
                name:
                    type: string
                type:
                    type: string
                    enum: ["application","product","database-user","schema","table","column"]
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
    - system
    '''
    node = request.get_json()
    state.add_vertex(node["name"],type=node["type"])
    return "ok"

@config.controller.route("/system-node", methods=['GET'])
def list_nodes():
    '''
    list system nodes
    ---
    parameters:
          - in: query
            type: string
            name: type
            required: true
            enum: ["application","product","database-user","schema","table","column"]
    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - system
    '''
    node_type = request.args.get("type")
    if node_type is None:
        return abort(400,"Type cannot be null")

    return json.dumps([key for key in state.get_vertexes_of_type(node_type)])


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
                        enum: ["contains","calls","uses","fk"]
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
    - system
    '''
    relation = request.get_json()
    result = state.add_edge(start=relation["start"], end=relation["end"], relation_type=relation["relation_type"])
    if result is RESPONSE_OK:
        return "ok"
    else:
        abort(400,result)


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


@config.controller.route("/system-node/<string:node>/direct-connections",methods=['GET'])
def get_direct_connections(node):
    '''
    get direct connections of node
    ---
    parameters:
        - in: path
          type: string
          name: node
          required: true
        - in: query
          type: string
          name: type
          required: false
          enum: ["application","product","database-user","schema","table","column"]
        - in: query
          name: relation-type
          required: false
          type: string
          enum: ["contains","calls","uses","fk"]
    responses:
            200:
                content:
                    text/plain:
                      schema:
                        type: string
    tags:
     - system
    '''
    vertex = state.get_vertex(node)
    type = request.args.get("type")
    relation_type = request.args.get("relation-type")
    if vertex is None:
        abort(404)
    connections = state.find_direct_connections(node,type,relation_type)
    return json.dumps(connections)