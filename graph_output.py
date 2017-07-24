def writeAsText(lines):
    f = open('output.plantuml', 'w')
    for line in lines:
        f.write(line+"\n")

def writeAsImage(lines):
    print("not implemented")
