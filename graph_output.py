def writeAsText(lines):
    f = open('output.plantuml', 'w')
    for line in lines:
        f.write(line+"\n")

def writeAsImage(lines):
    #cat test.txt|java -jar plantuml.1.2017.15.jar -pipe > somefile.png
