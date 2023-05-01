from .config import Config
from .data_wrapper import DataWrapper

class RunObject:
    def __init__(self, run_id):
        self.id = run_id
        self.dir_path = f"runs/{self.id}"
        self.config_path = f"{self.dir_path}/metadata.json"
        self.data_path = f"{self.dir_path}/{self.id}.csv"
    
    @property
    def config(self):
        return Config(self.config_path)
    
    @property
    def data(self):
        return DataWrapper(self.data_path)