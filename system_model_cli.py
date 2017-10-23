import system_model_output as smo
import system_model_input as smi
import system_model as sm
import system_model_visualizer as svm

def drawComponentModel():
    f = open('output-cm.png', 'wb')
    inputSystemGraph = sm.component_model(smi.getSystemGraph())
    lines = svm.component_model_visualizer(inputSystemGraph).draw()
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)

def drawDatamodel():
    f = open('output-dm.png', 'wb')
    inputSystemGraph = sm.data_model(smi.getDatamodelGraph())
    lines = svm.datamodel_visualizer(inputSystemGraph).draw(colapsed_columns=True)
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)

drawDatamodel()
drawComponentModel()