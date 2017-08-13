from flask import Flask
import graph_output
import system_graph
import graph_visualizer
from flask import abort
from flask import request
from flask import send_file

app = Flask(__name__)

@app.route("/context-diagram/format=<string:format>",methods=['POST'])
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

@app.route("/context-diagram/global-graph/vertex/",methods=['POST'])
def add_new_vertex():
    # idea

if __name__ == "__main__":
    app.run()