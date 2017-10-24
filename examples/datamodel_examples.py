import system_model_output as smo
import system_model as sm
import system_model_visualizer as svm


def get_datamodel_graph():
    return {
        "vertexes":{
        "TABLE1":{"type":"table"},
        "TABLE2":{"type":"table"},
        "SCHEMA1":{"type":"schema"},
        "T1_ID":{"type":"column"},
        "T1_PROPERTY1":{"type":"column"},
        "T1_T2_FK":{"type":"column"},
        "T2_ID":{"type":"column"},
        "T2_PROPERTY1":{"type":"column"}
        },
        "edges":[
            {"start":"T1_ID","end":"TABLE1"},
            {"start":"T1_PROPERTY1","end":"TABLE1"},
            {"start":"T1_T2_FK","end":"TABLE1"},
            {"start":"T1_T2_FK","end":"T2_ID","relation_type":"fk"},
            {"start":"T2_ID","end":"TABLE2"},
            {"start":"T2_PROPERTY1","end":"TABLE2"},
            {"start":"TABLE1","end":"SCHEMA1"},
            {"start":"TABLE2","end":"SCHEMA1"},
    ]}


def draw_datamodel():
    f = open('output-dm.png', 'wb')
    inputSystemGraph = sm.data_model(get_datamodel_graph())
    lines = svm.datamodel_visualizer(inputSystemGraph).draw(colapsed_columns=False)
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)

draw_datamodel()