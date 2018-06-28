import subprocess
import io
import os
import requests


def writeAsFile(lines, file='output.plantuml'):
    f = open(file, 'w')
    content = writeAsText(lines)
    f.write(content)
    f.close()


class PlantUmlRenderer():
    def render_image(self, input, input_format="lines"):
        pass


class PlantUmlServerRenderer(PlantUmlRenderer):
    def __init__(self, server_url):
        self.render_png_url = server_url + "/plantuml/png"

    def render_image(self, input, input_format="lines"):
        if input_format == "lines":
            content = writeAsText(input)
        else:
            content = input
        result = requests.post(self.render_png_url,
                               data=content)
        if result.status_code != 200:
            return None
        return io.BytesIO(result.content)


class PlantUmlLocalRenderer(PlantUmlRenderer):
    def render_image(self, input, input_format="lines"):
        if input_format == "lines":
            content = writeAsText(input)
            content = bytes(content, "UTF-8")
        else:
            content = input
        plant_uml_location = os.environ["PLANT_UML"]
        p = subprocess.Popen(["java", "-jar", "-DPLANTUML_LIMIT_SIZE=16384", plant_uml_location, "-pipe"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        result = p.communicate(content)
        result = self.__trim_left_png__(result[0])

        return io.BytesIO(result)

    @staticmethod
    def __trim_left_png__(png: bytes):
        index = png.find(b'PNG')
        index = png[0:index].rfind(b'\n')
        return png[index + 1:]


image_renderer = PlantUmlServerRenderer("http://localhost:8090")


def render_image(input, input_format="lines"):
    return image_renderer.render_image(input, input_format)


def writeAsText(lines):
    return "\n".join(lines)
