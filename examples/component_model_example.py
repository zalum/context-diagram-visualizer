from smv import system_model_visualizer as svm, system_model_output as smo, system_model as sm


def get_component_graph():
    return {"vertexes":{
            "precedingapp":{"name":"precedingapp","type":"application"},
            "app1":{"name": "app1","type":"application"},
            "app2":{"name":"app2","type":"application"},
            "app3":{"name":"app3","type":"application"},
            "product":{"name": "product","type":"product"}
            },
            "edges":[
                {"start":"precedingapp","end":"app1","relation_type":"calls"},
                {"start":"app1","end":"app2","relation_type":"calls"},
                {"start":"app2","end":"product","relation_type":"contains"},
                {"start":"app1","end":"product","relation_type":"contains"},
                {"start":"app2","end":"app3","relation_type":"calls"},
                {"start":"app3","end":"product","relation_type":"contains"}
                ]}


def draw_component_model():
    f = open('output-cm.png', 'wb')
    inputSystemGraph = sm.component_model(get_component_graph())
    lines = svm.component_model_visualizer(inputSystemGraph).draw()
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)

draw_component_model()