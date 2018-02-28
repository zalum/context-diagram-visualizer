from smv import c4_diagram
from smv import datamodel_diagram
from smv.core.model import system_models_repository
from smv.core.model.system_model import data_model as data_model
from smv.core.model.system_model import system_model as system_model
from smv.core.model.system_model_visualizer import datamodel_visualizer
from smv.core.infrastructure.system_model_output import render_image
from smv.core.infrastructure.system_model_output import writeAsText
from smv.core.model.system_model_visualizer import component_model_visualizer as cmv
from smv.core.model.system_model_visualizer import datamodel_visualizer as dmv
from smv.core import *
import json


def add_system_node(system_node_id, system_node_type):
    return system_models_repository.add_system_node(system_node_id, system_node_type=system_node_type)


def append_json(json_content):
    graph = json.loads(json_content)
    model = system_model(graph)
    system_models_repository.append_system_model(model)


def render_component_diagram(component,output_format):
    model = c4_diagram.search(component)
    markdown = cmv(model).draw()
    return _render_diagram_from_system_model(model,markdown,output_format)


def render_datamodel_diagram(database_user, output_format, collapsed_columns=False):
    model = datamodel_diagram.search_database_user(database_user)
    markdown = dmv(model).draw(collapsed_columns)
    return _render_diagram_from_system_model(model, markdown, output_format)


def render_datamodel_diagram_from_plantuml(plantuml, output_format)->Response:
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.json:
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.text:
        return Response.success(writeAsText(plantuml))
    if output_format == SupportedOutputFormats.image:
        return Response.success(render_image(plantuml))


def render_datamodel_diagram_from_json(json_content, output_format)->Response:
    graph = json.loads(json_content)
    model = data_model(graph)
    markdown = datamodel_visualizer(model).draw()
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.text:
        return Response.success(writeAsText(markdown))
    if output_format == SupportedOutputFormats.image:
        return Response.success(render_image(markdown))
    if output_format == SupportedOutputFormats.json:
        return Response.success(json_content)

def _render_diagram_from_system_model(model, markdown, output_format):
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.json:
        return Response.success(model.graph)
    if output_format == SupportedOutputFormats.text:
        return Response.success(writeAsText(markdown))
    if output_format == SupportedOutputFormats.image:
        return Response.success(render_image(markdown))

