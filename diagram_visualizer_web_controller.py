import graph_output
import system_graph
import graph_visualizer
from flask import abort
from flask import request
from flask import send_file
from flask import Blueprint

context_diagram_controller = Blueprint('context-diagram', 'context-diagram')

@context_diagram_controller.route("/format=<string:format>",methods=['POST'])
def get_product_graph(format="text"):
    inputSystemGraph = system_graph.SystemGraph(request.get_json())
    lines = graph_visualizer.ContextDiagramGraphVisualizer(inputSystemGraph).draw()
    if format == "text":
        return graph_output.writeAsText(lines)
    else:
        if format == "image":
            return send_file(graph_output.writeAsImage(lines),mimetype="image/jpeg")
        else:
            abort(406)

@context_diagram_controller.route("/global-graph/vertex/",methods=['POST'])
def add_new_vertex():
    abort(406)