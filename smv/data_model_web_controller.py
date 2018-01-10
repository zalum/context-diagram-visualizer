import json

from flask import Blueprint
from flask import abort
from flask import request

from smv import web_utils, system_model_visualizer as smv, system_model as sm
from smv.search_model import find_connected_graph
from smv.search_model import search_criteria
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
    criteria = search_criteria().with_include_vertex_types(0, ["table"]). \
        with_include_vertex_types(1, ["column"]). \
        with_include_relation_types(2, ["fk"]). \
        with_include_vertex_types(3, ["table"]).\
        with_include_vertex_types(4, ["schema"])

    schema_datamodel = sm.data_model(find_connected_graph(state,schema,criteria=criteria,level=5).graph)
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
    criteria = search_criteria().with_include_vertex_types(0,["table"]).\
        with_include_vertex_types(1, ["schema", "column"]). \
        with_include_relation_types(2, ["fk"]).\
        with_include_vertex_types(3, ["table"])

    data_model = sm.data_model(find_connected_graph(state,user, level=4, criteria=criteria).graph)
    diagram = smv.datamodel_visualizer(data_model).draw()
    return build_diagram_response(diagram, request.args.get("format") if "format" in request.args else "image")
