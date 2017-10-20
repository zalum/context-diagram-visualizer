import graph_output
import graph_input
import system_model as sm
import system_model_visualizer as svm

def drawSystemGraph():
    inputSystemGraph = sm.application_model(graph_input.getSystemGraph())
    lines = svm.ContextDiagramGraphVisualizer(inputSystemGraph).draw()
    graph_output.writeAsImage(lines)

def drawDatamodel():
    f = open('output.png', 'wb')
    inputSystemGraph = sm.data_model(graph_input.getDatamodelGraph())
    lines = svm.DatamodelVisualizer(inputSystemGraph).draw(colapsed_columns=True)
    print(lines)
    picture = graph_output.writeAsImage(lines).getvalue()
    f.write(picture)

drawDatamodel()