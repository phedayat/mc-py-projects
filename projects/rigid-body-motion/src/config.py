from json import dump, load

class Config:
    def __init__(self):
        self.config = self._get_config()

    def save(self):
        self._save_config()

    def __getitem__(self, key):
        return self.config[key]
    
    def __setitem__(self, key, value):
        self.config[key] = value

    def _get_config(self):
        with open("/config.json") as f:
            config_obj = load(f)
            return config_obj

    def _save_config(self):
        with open("/config.json", "w") as f:
            dump(self.config, f, indent=4)
