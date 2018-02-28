import subprocess
import io
import os


def writeAsFile(lines, file='output.plantuml'):
    f = open(file, 'w')
    content = writeAsText(lines)
    f.write(content)
    f.close()


def render_image(input, input_format="lines"):
    if input_format == "lines":
        content = writeAsText(input)
        content = bytes(content, "UTF-8")
    else:
        content = input
    plant_uml_location = os.environ["PLANT_UML"]
    p = subprocess.Popen(["java", "-jar", "-DPLANTUML_LIMIT_SIZE=16384", plant_uml_location, "-pipe"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    result = p.communicate(content)
    result = trim_left_png(result[0])

    return io.BytesIO(result)


def trim_left_png(png:bytes):
    index = png.find(b'PNG')
    index = png[0:index].rfind(b'\n')
    return png[index+1:]


def writeAsText(lines):
    return "\n".join(lines)






