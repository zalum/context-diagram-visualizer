import subprocess
import io
import os


def writeAsFile(lines, file='output.plantuml'):
    f = open(file, 'w')
    content = writeAsText(lines)
    f.write(content)
    f.close()


def writeAsImage(lines):
    plant_uml_location = os.environ["PLANT_UML"]
    p = subprocess.Popen(["java", "-jar", "-DPLANTUML_LIMIT_SIZE=16384", plant_uml_location, "-pipe"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    content = writeAsText(lines)
    result = p.communicate(bytes(content, "UTF-8"))
    result = trim_left_png(result)
    return io.BytesIO(result)


def writeAsText(lines):
    return "\n".join(lines)


def trim_left_png(png:io.BytesIO):
    index = png.find(b'PNG')
    index = png[0:index].rfind(b'\n')
    return png[index+1:]



