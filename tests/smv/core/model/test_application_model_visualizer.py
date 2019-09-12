import unittest

from smv.core.model import system_model as sm, system_model_visualizer as svm


class ComponentModelVisualizerTest(unittest.TestCase):
    def testDrawOneRelation(self):
        model = sm.component_model()
        model.add_system_node("1",type = "application",name = "app1")
        model.add_system_node( "2",type = "application",name = "app2")
        model.add_relation(start="1", end="2", relation_type="calls")
        expectedResult =["@startuml","left to right direction","[app1]-->[app2]","@enduml"]
        self.__run_draw_context_diagram_test__(model, expectedResult)

    def testDrawProductWithOneApp(self):
        model = sm.component_model()
        model.add_system_node("1",type = "product",name = "app1")
        model.add_system_node("2",type = "application",name = "app2")
        model.add_relation(start="2", end="1", relation_type="contains")
        expectedResult =["@startuml","left to right direction","folder app1{","[app2]","}","@enduml"]
        self.__run_draw_context_diagram_test__(model, expectedResult)

    def testDrawProductWithOneAppWithUnidirectionalRelation(self):
        model = sm.component_model()
        model.add_system_node("1",type = "application",name = "app1")
        model.add_system_node("2",type = "product",name = "product")
        model.add_relation(start="2", end="1", relation_type="contains")
        expectedResult =["@startuml","left to right direction","folder product{","[app1]","}","@enduml"]
        self.__run_draw_context_diagram_test__(model, expectedResult)

    def testProductWithDependencyToApp(self):
        model = sm.component_model()
        model.add_system_node("1",type = "application",name = "app1")
        model.add_system_node("2",type = "product",name = "product")
        model.add_system_node("3",type = "application",name = "app2")
        model.add_relation(start="1", end="2", relation_type="contains")
        model.add_relation(start="1", end="3", relation_type="calls")
        expectedResult =["@startuml","left to right direction","folder product{","[app1]","}","[app1]-->[app2]","@enduml"]
        self.__run_draw_context_diagram_test__(model, expectedResult)

    def testNameEscaping(self):
        model = sm.component_model()
        model.add_system_node("1",type = "application",name = "app 1")
        model.add_system_node("2",type = "product",name = "product 1")
        model.add_system_node("3",type = "application",name = "app 2")
        model.add_relation(start="1", end="2", relation_type="contains")
        model.add_relation(start="1", end="3", relation_type="calls")
        expectedResult =["@startuml","left to right direction","folder product_1{","[app 1]","}","[app 1]-->[app 2]","@enduml"]
        self.__run_draw_context_diagram_test__(model, expectedResult)

    def __run_draw_context_diagram_test__(self, model, expectedResult):
        result = svm.component_model_visualizer(model).draw()
        self.assertListEqual(expectedResult,result)

