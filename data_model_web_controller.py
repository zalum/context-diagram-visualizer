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
    url_prefix="/data-model"
)


@config.controller.route("/",methods=['GET'])
def list_database_objects():
    """
    list database objects
    ---
    parameters:
      - in: query
        name: type
        type: string
        enum: ["database-user","schema","table","column"]
    responses:
        200:
          description: list database objects
    tags:
    - datamodel
    """
    database_object_type = request.args.get("type")
    return json.dumps([key for key in state.get_vertexes_of_type(database_object_type)])


@config.controller.route("/user/<string:user>", methods=['POST'])
def add_new_user(user):
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
          description: Created a database user
    tags:
    - datamodel
    """
    state.add_vertex(user,"database-user")
    return "ok"

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
    connected_graph = state.find_connected_graph(user)
    diagram = smv.datamodel_visualizer(sm.data_model(connected_graph.graph)).draw()
    return build_diagram_response(diagram, "image")


@config.controller.route("/user/<string:user>", methods=['GET'])
def get_db_user(user):
    """
    get db user
    ---
    parameters:
      - in: path
        required: true
        name: user
        type: string
    tags:
    - datamodel
    responses:
        200:
          description: get db user
    """
    return json.dumps(state.find_connected_graph(user).graph)


@config.controller.route("/relation", methods=['POST'])
def create_relation():
    """
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
                        enum: ["contains","fk"]
                examples:
                    fk:
                        start: column1
                        end: column2
                        relation_type: fk
    responses:
        200:
            content:
                text/plain:
                  schema:
                    type: string
    tags:
    - datamodel
    """
    relation = request.get_json()
    if not state.has_vertex(relation["start"]):
        return abort(404, "Vertex {} is missing".format(relation["start"]))
    if not state.has_vertex(relation["end"]):
        return abort(404, "Vertex {} is missing".format(relation["end"]))

    state.add_edge(start=relation["start"],
                   end=relation["end"],
                   relation_type=relation["relation_type"])
    return "ok"
