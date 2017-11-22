from smv import system_model_visualizer as svm, system_model_output as smo, system_model as sm


def get_component_graph():
    return {"vertexes":{
            "1":{"name":"precedingapp","type":"application"},
            "2":{"name": "app1","type":"application"},
            "3":{"name":"app2","type":"application"},
            "4":{"name":"app3","type":"application"},
            "5":{"name": "product","type":"product"}
            },
            "edges":[
                {"start":"1","end":"2","relation_type":"calls"},
                {"start":"2","end":"3","relation_type":"calls"},
                {"start":"3","end":"5","relation_type":"contains"},
                {"start":"2","end":"5","relation_type":"contains"},
                {"start":"3","end":"4","relation_type":"calls"},
                {"start":"4","end":"5","relation_type":"contains"}
                ]}


def draw_component_model():
    f = open('output-cm.png', 'wb')
    inputSystemGraph = sm.component_model(get_component_graph())
    lines = svm.component_model_visualizer(inputSystemGraph).draw()
    picture = smo.writeAsImage(lines).getvalue()
    f.write(picture)

draw_component_model()