# diagram visualizer
It generates 2 types of graphs: context and datamodels

## Scope
from your landscape you can extract a graph of your system or datamodel and pipe it to this utility. It will spit a plantuml markdown

## Prerequisites
python3
plantuml
requests module

## How to run
python3 diagram-visualizer-cli.py
generates plantuml markdown and/or pictures

python3 diagram-visualizer-web.py
it exposes an endpoint

## Backlog
put a swagger docu on the endpoint
