import os
import yaml

config = {}

NEO4J_DB = "neo4j_db"
FILE_SYSTEM_DB = "in_memory_db"


NEO4J_URL = "neo4j-url"
PERSISTANCE_ENGINE = "persistance-engine"
PLANT_UML_SERVER = "plantuml-server"
PLANT_UML_LOCAL_JAR = "plantuml-local-jar"

properties = [PERSISTANCE_ENGINE, PLANT_UML_SERVER, PLANT_UML_LOCAL_JAR]


def load_defaults():
    config[PERSISTANCE_ENGINE] = NEO4J_DB


def load_config_file():
    global config
    if "CONFIG_LOCATION" not in os.environ:
        return

    with open(os.environ["CONFIG_LOCATION"], 'r') as stream:
        try:
            config.update(yaml.load(stream))
        except yaml.YAMLError as e:
            raise Exception("Error parsing config file", e)


def load_from_environment():
    for property in properties:
        if property in os.environ:
            config[property] = os.environ[property]


def load_configs():
    load_defaults()
    load_config_file()
    load_from_environment()


load_configs()



