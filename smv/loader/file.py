import yaml
import json
from smv.core.model.system_model import system_model


def __load_json(file_path):
    file = open(file_path)
    return json.loads("".join(file.readlines()))


def _load_yaml(file_path):
    file = open(file_path)
    return yaml.load(file, Loader=yaml.Loader)


__loaders = dict(
    yaml=lambda file_path: _load_yaml(file_path),
    json=lambda file_path: __load_json(file_path)
)


def __get_file_type(file_path):
    extension_search = file_path.split(".")
    extension_search.reverse()
    return extension_search[0]


def load(file_path: str):
    file_type = __get_file_type(file_path)
    if file_type not in __loaders:
        raise Exception("File type {} is not loadable.".format(file_type))
    file_content = __loaders[file_type](file_path)
    return system_model(file_content)


def load_files(file_paths: list):
    model = system_model()
    for file_path in file_paths:
        model_from_file = load(file_path)
        model.append(model_from_file)
    return model


def __get_file_type(file_path):
    extension_search = file_path.split(".")
    extension_search.reverse()
    return extension_search[0]


def load(file_path: str):
    file_type = __get_file_type(file_path)
    if file_type not in __loaders:
        raise Exception("File type {} is not loadable.".format(file_type))
    file_content = __loaders[file_type](file_path)
    return system_model(file_content)


def load_files(file_paths: list):
    model = system_model()
    for file_path in file_paths:
        model_from_file = load(file_path)
        model.append(model_from_file, partial_append=True)
    return model
