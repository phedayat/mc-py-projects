import json

class Config:
    def __init__(self, config):
        self.config = self._get_config_obj(config)

    def get(self, key):
        if key in self.config:
            return self.config[key]
        return None

    def _get_config_obj(self, config_path):
        with open(config_path) as config:
            return json.load(config)
