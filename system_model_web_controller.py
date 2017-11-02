import system_model as sm
import system_model_visualizer as smv
import system_model_output as smo
import web_utils

from flask import abort
from flask import request
from flask import send_file
from flask import Blueprint
import json

config = web_utils.web_controller_config(
    controller = Blueprint('system-model', 'system-model'),
    swagger_config = dict(endpoint = "system-model",
                          route = "/system-model.json",
                          rule_filter=lambda rule: web_utils.rule_filter(rule,['/datamodel','/c4'])
                          ),
    url_prefix="/system-diagram"
)

_datamodels={}


def _build_diagram_response(output, format):
    if format == "text":
        return smo.writeAsText(output)
    else:
        if format == "image":
            return send_file(smo.writeAsImage(output), mimetype="image/png")
        else:
            abort(406)

@config.controller.route("/format=<string:format>", methods=['POST'])
def get_product_graph(format="text"):
    inputSystemGraph = sm.component_model(request.get_json())
    lines = smv.component_model_visualizer(inputSystemGraph).draw()
    return _build_diagram_response(lines,format)

@config.controller.route("/datamodel/<string:datamodel>", methods=['POST'])
def add_new_datamodel(datamodel):
    """
    create a datamodel
    ---
    parameters:
    - in: path
      name: datamodel
      required: true
      type: string
    responses:
        200:
          description: Created a datamodel
    tags:
    - datamodel
    """
    _datamodels[datamodel]=system_graph.data_model()
    return _datamodels[datamodel].to_json()


@config.controller.route("/datamodel/<string:datamodel>", methods=['DELETE'])
def delete_datamodel(datamodel):
    """
    delete datamodel
    ---
    parameters:
    - in: path
      name: datamodel
      required: true
      type: string
    responses:
      200:
        description: Created a datamodel
    tags:
    - datamodel
    """
    _datamodels.pop(datamodel)
    return _datamodels.keys()

@config.controller.route("/datamodel/<string:datamodel>/schema/<string:schema>", methods=['POST'])
def add_new_schema(datamodel,schema):
    """
    create schema
    ---
    parameters:
    - in: path
      name: datamodel
      required: true
      type: string
    - in: path
      name: schema
      required: true
      type: string
    responses:
        200:
          description: Created a schema
    tags:
    - schema
    """
    _datamodels[datamodel].add_schema(schema)
    return _datamodels[datamodel].to_json()

@config.controller.route("/datamodel/<string:datamodel>/schema/<string:schema>/table", methods=['POST'])
def add_table(datamodel,schema):
    """
    create table
    ---
    parameters:
    - in: path
      name: datamodel
      required: true
      type: string
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
          table_name:
            type: string
          columns:
            type: array
        examples:
          simple-example:
            table_name: USER
            columns: [ID,NAME,ACTIVE]
    tags:
    - table
    responses:
        200:
          description: Created a table
    """
    table = request.get_json()
    table_name = table["table_name"]
    graph = _datamodels[datamodel] # :type: system_graph:DatamodelGraph
    graph.add_table(table_name,schema)
    [graph.add_column(column,table_name) for column in table["columns"]]
    return graph.to_json()

@config.controller.route("/datamodel/", methods=['GET'])
def list_datamodels():
    """
    List datamodels
    ---
    responses:
        200:
            content:
            text/plain:
              schema:
                type: string
    tags:
    - datamodel
    """
    return json.dumps(list(_datamodels.keys()))

@config.controller.route("/datamodel/<string:datamodel>", methods=['GET'])
def draw_datamodel(datamodel):
    """
    Draw a datamodel
    ---
    parameters:
    - in: path
      name: datamodel
      required: true
      type: string
    - in: query
      name: format
      required: true
      type: string
      enum: [image,text]
    responses:
        200:
          content:
            image/png:
              schema:
                type: file
                format: binary
            text/plain:
              schema:
                type: string
    tags:
    - datamodel
    """
    output = smv.datamodel_visualizer(_datamodels[datamodel]).draw()
    return _build_diagram_response(output,request.args.get("format"))