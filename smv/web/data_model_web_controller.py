from flask import Blueprint
from flask import abort
from flask import request

from smv.core.actions import render_datamodel_diagram, render_datamodel_diagram_from_graph
from smv.core.model import system_model as sm
from smv.core.model import system_models_repository
from smv.web import web_utils
from smv.web.web_utils import build_response

config = web_utils.web_controller_config(
    controller = Blueprint('datamodel', 'datamodel'),
    url_prefix="/data-model"
)


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
    state = system_models_repository.get_full_system_model()
    if state.has_system_node(schema) is False:
        return abort(404,"Schema {} does not exist".format(schema))
    table_name = table["name"]
    table_model = sm.data_model()
    table_model.add_system_node(table_name, "table")
    [table_model.add_column(column,table_name) for column in table["columns"]]
    state.append(table_model)
    state.add_relation(start=schema, end=table_name, relation_type="contains")
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
        enum: ["image","test","json"]
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
    - datamodel
    """
    output_format = request.args.get("format")
    render_result = render_datamodel_diagram(user, output_format)
    return build_response(render_result,output_format)


@config.controller.route("/diagram", methods=['POST'])
def render_diagram():
    '''
    render a datamodel diagram from graph
    ---
    parameters:
    - in: query
      type: string
      name: input_format
      enum: ["json","yaml"]
      required: true
    - in: query
      type: string
      name: output_format
      enum: ["image","text"]
      default: "image"
      required: true
    - in: body
      name: graph
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
    - datamodel
    '''
    output_format = request.args.get("output_format")
    input_format = request.args.get("input_format")
    response = render_datamodel_diagram_from_graph(request.data, input_format = input_format, output_format=output_format)
    return web_utils.build_response(response, output_format)

