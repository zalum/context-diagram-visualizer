from flask import Flask
from diagram_visualizer_web_controller import context_diagram_controller

app = Flask(__name__)
app.register_blueprint(context_diagram_controller,url_prefix = "/context-diagram")

if __name__ == "__main__":
    app.run()
