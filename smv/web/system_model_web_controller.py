import io
import json

from flask import Blueprint
from flask import abort
from flask import request
from flask import send_file

import smv.core.actions as actions
from smv.core import *
from smv.core.model import system_models_repository
from smv.core.model.system_model import RESPONSE_OK_deprecated
from smv.web import web_utils

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
      - in: query
        type: number
        name: level
        required: false
    responses:
        200:
            content:
                application/json:
                  schema:
                    type: string
    tags:
    - system
    '''
    level = request.args.get("level")
    if level is not None:
        level = int(level)
    state = system_models_repository.get_full_system_model()
    return system_models_repository.find_connected_graph(state,node,level=level).to_string()

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
                application/json:
                  schema:
                    type: string
    tags:
    - system
    '''
    state = system_models_repository.get_full_system_model()
    return json.dumps(state.get_system_node(node), indent=2)


@config.controller.route("", methods=['POST'])
def append_model():
    '''
    append a system model to the state
    ---
    parameters:
       - in: body
         name: system_model
         required: true
         schema:
             type: object
             properties:
                system-nodes:
                    type: object
                    properties:
                        system-node:
                            type: object
                            properties:
                                type:
                                    type: string
                relations:
                    type: array
                    items:
                        type: object
                        properties:
                            start:
                                type: string
                            end:
                                type: string
                            relation-type:
                                type: string

    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - system
    '''
    result = actions.append_json(request.data)
    return web_utils.build_response(result, SupportedOutputFormats.json)


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
          - in: query
            type: string
            name: format
            required: false
            enum: ["id","full"]
            default: "full"
    responses:
        200:
            content:
                application/json:
                  schema:
                    type: string
    tags:
    - system
    '''
    node_type = request.args.get("type")
    format = request.args.get("format")
    if node_type is None:
        return abort(400,"Type cannot be null")
    state = system_models_repository.get_full_system_model()
    nodes = state.get_system_nodes_of_type(node_type)
    if format == "full":
        result = dict()
        for key in nodes:
            result[key] = state.get_system_node(key)
        return json.dumps(result,indent = 2)
    else:
        return json.dumps([key for key in nodes])


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
    state = system_models_repository.get_full_system_model()
    content = state.to_string()
    f.write(content)
    f.close()
    return "ok"

@config.controller.route("/state/", methods=['GET'])
def download_state():
    """
    get the state of the system in a file
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
    state = system_models_repository.get_full_system_model()
    content = state.to_string()
    return send_file(io.BytesIO(bytes(content,"UTF-8")), mimetype="text/plain")


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
    state = system_models_repository.get_full_system_model()
    vertex = state.get_system_node(node)
    type = request.args.get("type")
    relation_type = request.args.get("relation-type")
    if vertex is None:
        abort(404)
    connections = state.find_direct_connections(node,type,relation_type)
    return json.dumps(connections)