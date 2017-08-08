import graph_output
import graph_input
import system_graph
import graph_visualizer

def drawSystemGraph():
    inputSystemGraph = system_graph.SystemGraph(graph_input.getSystemGraph())
    lines = graph_visualizer.GraphVisualizer(inputSystemGraph).draw()
    graph_output.writeAsImage(lines)

def drawDatamodel():
    f = open('output.png', 'wb')
    inputSystemGraph = system_graph.DatamodelGraph(graph_input.getDatamodelGraph())
    lines = graph_visualizer.DatamodelVisualizer(inputSystemGraph).draw()
    print(lines)
    picture = graph_output.writeAsImage(lines).getvalue()
    f.write(picture)

drawDatamodel()