from flask import abort
from flask import send_file

from smv import system_model_output as smo


def rule_filter(matchers):
    return lambda rule: len([matcher for matcher in matchers if matcher in rule.rule]) != 0


class web_controller_config:
    def __init__(self,controller,url_prefix):
        self.controller = controller
        self.url_prefix = url_prefix


def build_diagram_response(diagram, output_format,input_format="lines"):
    if output_format == "plantuml":
        return smo.writeAsText(diagram)
    else:
        if output_format == "image":
            return send_file(smo.writeAsImage(diagram,input_format), mimetype="image/png")
        else:
            abort(406,'type not supported')