import system_model_output as smo
import system_model_input as smi
import system_model as sm
import system_model_visualizer as svm

def drawSystemGraph():
    inputSystemGraph = sm.application_model(smi.getSystemGraph())
    lines = svm.component_model_visualizer(inputSystemGraph).draw()
    smo.writeAsImage(lines)

def drawDatamodel():
    f = open('output.png', 'wb')
    inputSystemGraph = sm.data_model(smi.getDatamodelGraph())
    lines = svm.datamodel_visualizer(inputSystemGraph).draw(colapsed_columns=True)
    print(lines)
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)

drawDatamodel()