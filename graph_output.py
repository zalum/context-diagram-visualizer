import subprocess

def writeAsText(lines):
    f = open('output.plantuml', 'w')
    content = _prepare_content(lines)
    f.write(content)


def writeAsImage(lines):
    f = open('output.jpg', 'w')
    p = subprocess.Popen(["java","-jar","/data/tools/plant-uml/plantuml.1.2017.15.jar","-pipe"],stdin=subprocess.PIPE,stdout = f)
    content = _prepare_content(lines)
    result = p.communicate(bytes(content,"UTF-8"))


def _prepare_content(lines):
    return "\n".join(lines)