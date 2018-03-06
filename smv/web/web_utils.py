import json

from flask import abort
from flask import send_file

from smv.core import *


def build_response(response:Response, output_format):
    if response.return_code == RESPONSE_OK:
        return _build_success_response(response.content, output_format)
    else:
        if response.return_code == RESPONSE_ERROR:
            return abort(400, response.content)


def rule_filter(matchers):
    return lambda rule: len([matcher for matcher in matchers if matcher in rule.rule]) != 0


class web_controller_config:
    def __init__(self,controller,url_prefix):
        self.controller = controller
        self.url_prefix = url_prefix


def _build_success_response(content, output_format):
    if output_format == SupportedOutputFormats.json:
        return json.dumps(content, indent=2)
    else:
        if output_format == SupportedOutputFormats.text:
            return content
        else:
            if output_format == SupportedOutputFormats.image:
                return send_file(content, mimetype="image/png")