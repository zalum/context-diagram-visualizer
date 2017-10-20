from flask import Flask
from flasgger import Swagger

from system_model_web_controller import config as sm_web

def init_api_specification(app):
    app.config['SWAGGER'] = {
        'title': 'System Model',
        'uiversion': 3
    }
    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config["specs"][0] = sm_web.swagger_config
    swagger_config["specs_route"] = "/api-docs/"
    Swagger(app, config=swagger_config)

app = Flask(__name__)
app.register_blueprint(sm_web.controller, url_prefix =sm_web.url_prefix)

init_api_specification(app)

if __name__ == "__main__":
    app.run()

