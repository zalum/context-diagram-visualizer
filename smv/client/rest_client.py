from smv.core.model.system_model import system_model
import requests


class RestClient:

    def __init__(self, server_url="http://localhost:8080"):
        self.server_url = server_url

    def append_model(self, model:system_model):
        url = self.server_url+"/system-model"
        result = requests.post(url=url, json=model.graph)
        return result

