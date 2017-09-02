from flask import Flask
from flasgger import Swagger

from diagram_visualizer_web_controller import system_diagram_controller

def init_api_specification(app):
    app.config['SWAGGER'] = {
        'title': 'System Diagram',
        'uiversion': 3
    }
    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config["specs"][0]["endpoint"] = "system-diagram"
    swagger_config["specs"][0]["route"] = "/system-diagram.json"
    swagger_config["specs_route"] = "/api-docs/"
    Swagger(app, config=swagger_config)

app = Flask(__name__)
app.register_blueprint(system_diagram_controller, url_prefix ="/system-diagram")

init_api_specification(app)

if __name__ == "__main__":
    app.run()

