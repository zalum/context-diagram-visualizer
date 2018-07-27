from smv.core import SupportedOutputFormats, Response
from smv.core.model import system_models_repository
from smv.core.model.system_model import data_model as data_model
from smv.core.model.system_model import system_model as system_model
from smv.core.model.system_model_visualizer import datamodel_visualizer
from smv.core.infrastructure.system_model_output import render_image
from smv.core.infrastructure.system_model_output import writeAsText
from smv.core.model.system_model_visualizer import component_model_visualizer as cmv
from smv.core.model.system_model_visualizer import datamodel_visualizer as dmv
from smv.core.model.diagram_search import search_database_user
from smv.core.model.diagram_search import search_component_diagram
import json
import yaml


def add_system_node(system_node_id, system_node_type):
    return system_models_repository.add_vertex(system_node_id, type=system_node_type)


def add_relation(start, end, relation_type)->Response:
    return system_models_repository.add_relation(start, end, relation_type)

def append_json(json_content):
    graph = json.loads(json_content)
    model = system_model(graph)
    system_models_repository.append_system_model(model)


def append_model(system_model:system_model):
    system_models_repository.append_system_model(system_model)


def render_component_diagram(component,output_format):
    model = search_component_diagram(component)
    markdown = cmv(model).draw()
    return __render_diagram_from_system_model(model, markdown, output_format)


def render_datamodel_diagram(database_user, output_format, collapsed_columns=False):
    model = search_database_user(database_user)
    markdown = dmv(model).draw(collapsed_columns)
    return __render_diagram_from_system_model(model, markdown, output_format)


def render_datamodel_diagram_from_plantuml(plantuml, output_format)->Response:
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.json:
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.text:
        return Response.success(plantuml)
    if output_format == SupportedOutputFormats.image:
        return render_image(plantuml,"block")


def __transform_to_model(graph_content, input_format):
    if input_format == "json":
        graph = json.loads(graph_content)
    else:
        if input_format == "yaml":
            graph = yaml.load(graph_content)
    return data_model(graph)


def render_datamodel_diagram_from_graph(graph_content, output_format, input_format="json")->Response:
    model = __transform_to_model(graph_content, input_format)

    markdown = datamodel_visualizer(model).draw()
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.text:
        return Response.success(writeAsText(markdown))
    if output_format == SupportedOutputFormats.image:
        return render_image(markdown)
    if output_format == SupportedOutputFormats.json:
        return Response.success(graph_content)


def __render_diagram_from_system_model(model, markdown, output_format):
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.json:
        return Response.success(model.graph)
    if output_format == SupportedOutputFormats.text:
        return Response.success(writeAsText(markdown))
    if output_format == SupportedOutputFormats.image:
        return render_image(markdown)

