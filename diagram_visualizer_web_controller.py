import graph_output
import system_graph
import graph_visualizer
from flask import abort
from flask import request
from flask import send_file
from flask import Blueprint
import json

system_diagram_controller = Blueprint('system-diagram', 'system-diagram')

"""
:type: dict[str,system_graph.DatamodelGraph]
"""
datamodels={}


def _build_diagram_response(output, format):
    if format == "text":
        return graph_output.writeAsText(output)
    else:
        if format == "image":
            return send_file(graph_output.writeAsImage(output), mimetype="image/png")
        else:
            abort(406)

@system_diagram_controller.route("/format=<string:format>", methods=['POST'])
def get_product_graph(format="text"):
    inputSystemGraph = system_graph.SystemGraph(request.get_json())
    lines = graph_visualizer.ContextDiagramGraphVisualizer(inputSystemGraph).draw()
    return _build_diagram_response(lines,format)

@system_diagram_controller.route("/datamodel/<string:datamodel>", methods=['POST'])
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
    datamodels[datamodel]=system_graph.DatamodelGraph()
    return datamodels[datamodel].to_json()


@system_diagram_controller.route("/datamodel/<string:datamodel>", methods=['DELETE'])
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
    datamodels.pop(datamodel)
    return datamodels.keys()

@system_diagram_controller.route("/datamodel/<string:datamodel>/schema/<string:schema>", methods=['POST'])
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
    datamodels[datamodel].add_schema(schema)
    return datamodels[datamodel].to_json()

@system_diagram_controller.route("/datamodel/<string:datamodel>/schema/<string:schema>/table", methods=['POST'])
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
    graph = datamodels[datamodel] # :type: system_graph:DatamodelGraph
    graph.add_table(table_name,schema)
    [graph.add_column(column,table_name) for column in table["columns"]]
    return graph.to_json()

@system_diagram_controller.route("/datamodel/<string:datamodel>", methods=['GET'])
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
    output = graph_visualizer.DatamodelVisualizer(datamodels[datamodel]).draw()
    return _build_diagram_response(output,request.args.get("format"))