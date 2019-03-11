import json
import os

class Config(object):
    def __init__(self):
        self._config = None
        config_path = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
        
        with open(config_path, 'r') as file:
            self._config = json.load(file)

    def get(self, prop):
        if prop not in self._config.keys():
            return None
        return self._config[prop]
