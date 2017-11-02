
def rule_filter(rule,matchers):
    return len([matcher for matcher in matchers if matcher in rule.rule]) != 0


class web_controller_config:
    def __init__(self,controller,swagger_config,url_prefix):
        self.controller = controller
        self.swagger_config = swagger_config
        self.url_prefix = url_prefix