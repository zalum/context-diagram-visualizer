import graph_output
import graph_input
import system_graph
import graph_visualizer

inputSystemGraph = system_graph.SystemGraph(graph_input.getSystemGraph())
lines = graph_visualizer.GraphVisualizer(inputSystemGraph).draw()
graph_output.writeAsText(lines)
graph_output.writeAsImage(lines)
