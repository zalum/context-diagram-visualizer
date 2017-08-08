import subprocess
import io

def writeAsFile(lines):
    f = open('output.plantuml', 'w')
    content = writeAsText(lines)
    f.write(content)


def writeAsImage(lines):
    p = subprocess.Popen(["java","-jar","/data/tools/plant-uml/plantuml.1.2017.15.jar","-pipe"],
                         stdin = subprocess.PIPE,stdout = subprocess.PIPE)
    content = writeAsText(lines)
    result = p.communicate(bytes(content,"UTF-8"))
    return io.BytesIO(result[0])


def writeAsText(lines):
    return "\n".join(lines)