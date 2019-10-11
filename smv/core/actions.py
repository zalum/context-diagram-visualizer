from smv.core import SupportedOutputFormats, Response
from smv.core.model import system_models_repository
from smv.core.model.system_model import data_model as data_model
from smv.core.model.system_model import system_model as system_model
from smv.core.model.system_model_visualizer import DatamodelVisualizer
from smv.core.model.system_model_visualizer import BoundedContextVisualizer
from smv.core.model.system_model_visualizer import ComponentModelVisualizer as cmv
from smv.core.model.system_model_visualizer import DatamodelVisualizer as dmv
from smv.core.model.diagram_search import search_database_user, search, SEARCH_BOUNDED_CONTEXT
from smv.core.model.diagram_search import search_component_diagram
from smv.core.model.system_models_repository import SearchCriteria
from smv.core.model.application_config import config, NEO4J_DB, PERSISTANCE_ENGINE
from smv.core.infrastructure.system_model_output import render_image
from smv.core.infrastructure.system_model_output import writeAsText
from smv.core.infrastructure.neo4j_system_model_repository import Neo4jSearchCriteria
import json
import yaml


def add_relation(start, end, relation_type) -> Response:
    return system_models_repository.add_relation(start, end, relation_type)


def find_connected_graph(system_node, level):
    return system_models_repository.find_connected_graph(system_node, level)


def find_direct_connections(node, type=None, relation_type=None):
    if config[PERSISTANCE_ENGINE] == NEO4J_DB:
        end_node_query = "()" if type is None else "(:{})".format(type)
        relation_query = "--" if relation_type is None else "-[:{}]-".format(relation_type)
        start_node_query = "({{system_node_id:'{start_node}'}})"
        match_clause = start_node_query + relation_query + end_node_query
        search_query = Neo4jSearchCriteria([match_clause])
    else:
        search_query = SearchCriteria().with_max_levels(1)
        if type is not None:
            search_query.with_include_vertex_types(0, [type])
        if relation_type is not None:
            search_query.with_include_relation_types(0, [relation_type])

    model = system_models_repository.search(node, search_query)  # type: system_model
    if model is None:
        return []
    nodes = model.get_system_nodes()
    if len(nodes) is 0:
        return nodes
    nodes.remove(node)
    return nodes


def append_json(json_content):
    graph = json.loads(json_content)
    model = system_model(graph)
    system_models_repository.append_system_model(model)
    return Response.success("Append succesfull.")


def add_table(schema, table):
    if system_models_repository.get_node(schema) is None:
        return Response.error("Schema {} does not exist".format(schema))
    table_name = table["name"]
    table_model = data_model()
    table_model.add_system_node(table_name, "table")
    [table_model.add_column(column, table_name, schema) for column in table["columns"]]
    system_models_repository.append_system_model(table_model)
    system_models_repository.add_relation(start=schema, end=table_name, relation_type="contains")
    return Response.success(table)


def append_model(system_model: system_model):
    system_models_repository.append_system_model(system_model)


def render_component_diagram(component, output_format):
    model = search_component_diagram(component)
    markdown = cmv(model).draw()
    return __render_diagram_from_system_model(model, markdown, output_format)


def render_datamodel_diagram(database_user, output_format, collapsed_columns=False):
    model = search_database_user(database_user)
    markdown = dmv(model).draw(database_user, collapsed_columns)
    return __render_diagram_from_system_model(model, markdown, output_format)


def render_bounded_context_diagram(bounded_context, output_format):
    model = search(bounded_context, SEARCH_BOUNDED_CONTEXT)
    markdown = BoundedContextVisualizer(model).draw(bounded_context)
    return __render_diagram_from_system_model(model, markdown, output_format)


def render_datamodel_diagram_from_plantuml(plantuml, output_format) -> Response:
    if not SupportedOutputFormats.is_in(output_format):
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.json:
        return Response.error("Format {} is not accepted".format(output_format()))
    if output_format == SupportedOutputFormats.text:
        return Response.success(plantuml)
    if output_format == SupportedOutputFormats.image:
        return render_image(plantuml, "block")


def __transform_to_model(graph_content, input_format):
    if input_format == "json":
        graph = json.loads(graph_content)
    else:
        if input_format == "yaml":
            graph = yaml.load(graph_content)
    return data_model(graph)


def render_datamodel_diagram_from_graph(graph_content, output_format, input_format="json") -> Response:
    model = __transform_to_model(graph_content, input_format)

    markdown = DatamodelVisualizer(model).draw()
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
