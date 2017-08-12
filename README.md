# diagram visualizer
This utility has the purpose to put in a graph model the dependencies of a system of all kinds (until now system lanscape, datamodel) and use it as input for plantuml to generate a corresponding diagram 

## Scope
from your landscape you can extract a graph of your system or datamodel and pipe it to this utility. It will spit a plantuml markdown

## Prerequisites
python3
plantuml
requests module
flask

## How to run
python3 diagram-visualizer-cli.py
generates plantuml markdown and/or pictures

python3 diagram-visualizer-web.py
it exposes an endpoint

## Backlog
put a swagger docu on the endpoint

## endpoints
