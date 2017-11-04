import system_model_output as smo
from flask import send_file
from flask import abort

def rule_filter(rule,matchers):
    return len([matcher for matcher in matchers if matcher in rule.rule]) != 0


class web_controller_config:
    def __init__(self,controller,swagger_config,url_prefix):
        self.controller = controller
        self.swagger_config = swagger_config
        self.url_prefix = url_prefix

def build_diagram_response(diagram, format):
    if format == "text":
        return smo.writeAsText(diagram)
    else:
        if format == "image":
            return send_file(smo.writeAsImage(diagram), mimetype="image/png")
        else:
            abort(406,'type not supported')