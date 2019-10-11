from smv.core.infrastructure import system_model_output as smo
from smv.core.model import system_model as sm, system_model_visualizer as svm


def get_component_graph():
    return {"system-nodes":{
            "precedingapp":{"name":"precedingapp","type":"application"},
            "app1":{"name": "app1","type":"application"},
            "app2":{"name":"app2","type":"application"},
            "app3":{"name":"app3","type":"application"},
            "product":{"name": "product","type":"product"}
            },
            "relations":[
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
    lines = svm.ComponentModelVisualizer(inputSystemGraph).draw()
    picture = smo.render_image(lines).getvalue()
    f.write(picture)

draw_component_model()