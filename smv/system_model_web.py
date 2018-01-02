from flasgger import Swagger
from flask import Flask

from smv.component_model_web_controller import config as cm_web
from smv.data_model_web_controller import config as dm_web
from smv.system_model_web_controller import config as sm_web
from smv.plantuml_web_controller import config as plantuml_web
from smv.web_utils import rule_filter


def get_swagger_config():
    return dict(endpoint="system-model",
                route="/system-model.json",
                rule_filter=rule_filter([cm_web.url_prefix, dm_web.url_prefix, sm_web.url_prefix,plantuml_web.url_prefix]))


def init_api_specification(app):
    app.config['SWAGGER'] = {
        'title': 'System Model',
        'uiversion': 3
    }
    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config["specs"][0] = get_swagger_config()
    swagger_config["specs_route"] = "/api-docs/"
    Swagger(app, config=swagger_config)


def main():
    app = Flask(__name__)
    app.register_blueprint(cm_web.controller, url_prefix=cm_web.url_prefix)
    app.register_blueprint(dm_web.controller, url_prefix=dm_web.url_prefix)
    app.register_blueprint(sm_web.controller, url_prefix=sm_web.url_prefix)
    app.register_blueprint(sm_web.controller, url_prefix=sm_web.url_prefix)
    app.register_blueprint(plantuml_web.controller, url_prefix=plantuml_web.url_prefix)
    init_api_specification(app)
    app.run()


if __name__ == "__main__":
    main()
