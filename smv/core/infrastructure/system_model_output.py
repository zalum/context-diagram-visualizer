import subprocess
import io
from smv.core.model.application_config import config
from smv.core.model.application_config import PLANT_UML_LOCAL_JAR
from smv.core.model.application_config import PLANT_UML_SERVER
import requests

from smv.core import Response


def writeAsFile(lines, file='output.plantuml'):
    f = open(file, 'w')
    content = writeAsText(lines)
    f.write(content)
    f.close()


class PlantUmlRenderer():
    def render_image(self, input, input_format="lines"):
        pass


class PlantUmlServerRenderer(PlantUmlRenderer):
    def __init__(self):
        self.render_png_url = config[PLANT_UML_SERVER] + "/png"

    def render_image(self, input, input_format="lines"):
        if input_format == "lines":
            content = writeAsText(input)
        else:
            content = input
        result = requests.post(self.render_png_url,
                               data=content)
        if result.status_code != 200:
            return Response.error("Plant uml server {} failed to generate with error code {}".
                                  format(self.render_png_url, result.status_code))
        return Response.success(io.BytesIO(result.content))


class PlantUmlLocalRenderer(PlantUmlRenderer):
    def render_image(self, input, input_format="lines"):
        if input_format == "lines":
            content = writeAsText(input)
            content = bytes(content, "UTF-8")
        else:
            content = input
        plant_uml_location = config[PLANT_UML_LOCAL_JAR]
        p = subprocess.Popen(["java", "-jar", "-DPLANTUML_LIMIT_SIZE=16384", plant_uml_location, "-pipe"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        result = p.communicate(content)
        result = self._trim_left_png(result[0])

        return  Response.success(io.BytesIO(result))

    @staticmethod
    def _trim_left_png(png: bytes):
        index = png.find(b'PNG')
        index = png[0:index].rfind(b'\n')
        return png[index + 1:]


__image_renderer = None

def render_image(input, input_format="lines"):
    image_renderer = PlantUmlServerRenderer()
    return image_renderer.render_image(input, input_format)

def writeAsText(lines):
    return "\n".join(lines)
