import graph_output
import system_graph
import graph_visualizer
from flask import abort
from flask import request
from flask import send_file
from flask import Blueprint
import json

class web_controller_config:
    def __init__(self,controller,swagger_config,url_prefix):
        self.controller = controller
        self.swagger_config = swagger_config
        self.url_prefix = url_prefix

def rule_filter(rule,matchers):
    return len([matcher for matcher in matchers if matcher in rule.rule]) != 0

config = web_controller_config(
    controller = Blueprint('system-model', 'system-model'),
    swagger_config = dict(endpoint = "system-model",
                          route = "/system-model.json",
                          rule_filter=lambda rule: rule_filter(rule,['/datamodel','/c4'])
                          ),
    url_prefix="/system-diagram"
)

__datamodels={}


def _build_diagram_response(output, format):
    if format == "text":
        return graph_output.writeAsText(output)
    else:
        if format == "image":
            return send_file(graph_output.writeAsImage(output), mimetype="image/png")
        else:
            abort(406)

@config.controller.route("/format=<string:format>", methods=['POST'])
def get_product_graph(format="text"):
    inputSystemGraph = system_graph.application_model(request.get_json())
    lines = graph_visualizer.ContextDiagramGraphVisualizer(inputSystemGraph).draw()
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
    __datamodels[datamodel]=system_graph.data_model()
    return __datamodels[datamodel].to_json()


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
    __datamodels.pop(datamodel)
    return __datamodels.keys()

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
    __datamodels[datamodel].add_schema(schema)
    return __datamodels[datamodel].to_json()

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
    graph = __datamodels[datamodel] # :type: system_graph:DatamodelGraph
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
    return json.dumps(list(__datamodels.keys()))

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
    output = graph_visualizer.DatamodelVisualizer(__datamodels[datamodel]).draw()
    return _build_diagram_response(output,request.args.get("format"))