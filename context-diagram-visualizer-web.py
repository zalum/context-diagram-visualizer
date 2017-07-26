from flask import Flask
import graph_input
import system_graph
import json
import graph_visualizer
from flask import abort
from flask import request

app = Flask(__name__)

@app.route("/product/format=<string:format>",methods=['POST'])
def get_product_graph(format="text"):
    print(request.data)
    inputSystemGraph = system_graph.SystemGraph(request.get_json())
    lines = graph_visualizer.GraphVisualizer(inputSystemGraph).draw()
    if format == "text":
        return str.join("\n",lines)
    else:
        if format == "image":
            abort(501)
        else:
            abort(406)


if __name__ == "__main__":
    app.run()