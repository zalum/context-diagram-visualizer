import system_model as sm
import system_model_visualizer as smv
import web_utils

from flask import abort
from flask import request
from web_utils import build_diagram_response
from flask import Blueprint
import json

from system_model_state import state

config = web_utils.web_controller_config(
    controller = Blueprint('datamodel', 'datamodel'),
    swagger_config = dict(endpoint = "datamodel",
                          route = "/system-model.json",
                          rule_filter=lambda rule: web_utils.rule_filter(rule,['/schema','/component'])
                          ),
    url_prefix="/data-model"
)


@config.controller.route("/user/<string:user>", methods=['POST'])
def add_new_datamodel(user):
    """
    create a database-user
    ---
    parameters:
    - in: path
      name: user
      required: true
      type: string
    responses:
        200:
          description: Created a datamodel
    tags:
    - datamodel
    """
    abort(501,"to be done")

@config.controller.route("/schema/<string:schema>/diagram", methods=["get"])
def draw_schema(schema):
    '''
    get diagram of schema
    ---
    parameters:
          - in: path
            type: string
            name: schema
            required: true
    responses:
        200:
          description: get diagram of schema
    tags:
    - datamodel
    '''
    schema_datamodel = state.find_connected_graph(schema)
    diagram = smv.datamodel_visualizer(sm.data_model(schema_datamodel.graph)).draw()
    return build_diagram_response(diagram,"image")

@config.controller.route("/schema", methods=['POST'])
def add_new_schema():
    """
    create schema
    ---
    parameters:
    - in: body
      name: schema
      required: true
      schema:
        type: object
        properties:
            name:
                type: string
    responses:
        200:
          description: Created a schema
    tags:
    - datamodel
    """
    schema = request.get_json()
    state.add_vertex(key=schema["name"],type="schema")
    return "ok"


@config.controller.route("/schema/<string:schema>", methods=['GET'])
def get_schema(schema):
    '''
    get schema structure
    ---
    parameters:
          - in: path
            type: string
            name: schema
            required: true
    responses:
        200:
          description: get schema structure
    tags:
    - datamodel
    '''
    schema_model = state.find_connected_graph(schema)
    return json.dumps(schema_model.graph)


@config.controller.route("/schema/<string:schema>/table", methods=['POST'])
def add_table(schema):
    """
    create table in schema
    ---
    parameters:
    - in: path
      name: schema
      required: true
      type: string
    - in: body
      name: table
      required: true
      schema:
        type: object
        properties:
          name:
            type: string
          columns:
            type: array
        examples:
          simple-example:
            table_name: USER
            columns: [ID,NAME,ACTIVE]
    tags:
    - datamodel
    responses:
        200:
          description: Created a table
    """
    table = request.get_json()
    if state.has_vertex(schema) is False:
        return abort(404,"Schema {} does not exist".format(schema))
    table_name = table["name"]
    table_model = sm.data_model()
    table_model.add_vertex(table_name,"table")
    [table_model.add_column(column,table_name) for column in table["columns"]]
    state.append(table_model)
    state.add_edge(start=schema,end=table_name,relation_type="contains")
    return "ok"