# System Model & Visualizer - SMV
This utility has the purpose to put in a graph model the dependencies of a system of all kinds
(until now system lanscape, datamodel) and use it as input for plantuml to generate a corresponding diagram

## Features
* model your system in a graph representation
* types of models
** component model for application applications, software products etc
** datamodel
* generates diagrams of your system using plantuml markdown
* exposes api endpoint to encourage colaboration

## Prerequisites
* python3, java
* plantuml as a jar
* requests module
* flask
* flasgger

## How to run
* python3 diagram-visualizer-cli.py
* python3 diagram-visualizer-web.py


## Backlog
* document c4 diagram of this utility
* plugin system for different sources of data: jira, aws, oracle etc
* improve validation and http error codes of endpoint
* enable state on this utility
* define a schema of the graph so users know what is possible
* use a graph database to store the graph & provide a query language
* deployment infrastructure: docker, etc

