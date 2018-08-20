import os

config = {}

NEO4J_DB = "neo4j_db"
FILE_SYSTEM_DB = "in_memory_db"

PERSISTANCE_ENGINE = "persistance-engine"
PLANT_UML_SERVER = "plantuml-server"
PLANT_UML_LOCAL_JAR = "plantuml-local-jar"

properties = [PERSISTANCE_ENGINE, PLANT_UML_SERVER, PLANT_UML_LOCAL_JAR]


def load_defaults():
    config[PERSISTANCE_ENGINE] = NEO4J_DB


def load_config_file():
    pass


def load_from_environment():
    for property in properties:
        if property in os.environ:
            config[property] = os.environ[property]


def load_configs():
    load_defaults()
    load_config_file()
    load_from_environment()


load_configs()



