from flask import Blueprint
from flask import abort
from flask import request

import smv.datamodel_diagram as datamodel_diagram
from smv import web_utils, system_model_visualizer as smv
from smv.core.model import system_model as sm
from smv.system_model_state import state
from smv.web_utils import build_diagram_response

config = web_utils.web_controller_config(
    controller = Blueprint('datamodel', 'datamodel'),
    url_prefix="/data-model"
)


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
          - in: query
            type: string
            name: format
            enum: ["image","plantuml.md"]
            default: ["image"]
            required: true
    responses:
        200:
          description: get diagram of schema
    tags:
    - datamodel
    '''
    schema_datamodel = datamodel_diagram.search_schema(schema)
    diagram = smv.datamodel_visualizer(schema_datamodel).draw()
    return build_diagram_response(diagram,request.args.get("format"))



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


@config.controller.route("/user/<string:user>/diagram", methods=['GET'])
def draw_db_user(user):
    """
    get db user diagram
    ---
    parameters:
      - in: path
        required: true
        name: user
        type: string
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
    - datamodel
    """
    data_model = datamodel_diagram.search_database_user(user)
    diagram = smv.datamodel_visualizer(data_model).draw()
    return build_diagram_response(diagram, request.args.get("format") if "format" in request.args else "image")
