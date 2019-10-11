from flask import Blueprint, request

from smv.core.actions import render_bounded_context_diagram
from smv.web import web_utils
from smv.web.web_utils import build_response

bc_web = web_utils.web_controller_config(
    controller=Blueprint('bounded-context', 'bounded-context'),
    url_prefix="/bounded-context")


@bc_web.controller.route("/<string:bounded_context>/diagram", methods=['GET'])
def draw_diagram(bounded_context):
    """
    get diagram of the bounded-context
    ---
    parameters:
      - in: path
        required: true
        name: bounded_context
        type: string
      - in: query
        type: string
        name: format
        enum: ["image","text","json"]
        default: "image"
        required: true
    responses:
        200:
            content:
                image/png:
                  schema:
                    type: file
                    format: binary
    tags:
    - bounded-context
    """
    output_format = request.args.get("format")
    render_result = render_bounded_context_diagram(bounded_context, output_format)
    return build_response(render_result, output_format)
