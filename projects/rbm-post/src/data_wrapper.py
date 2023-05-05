import pandas as pd

from dataclasses import dataclass

@dataclass
class IMUEntry:
    index: int
    time: int
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float

class DataWrapper:
    def __init__(self, data_path):
        self.path = data_path
        self.df = pd.read_csv(self.path, delimiter=",", index_col="index")

class DataExctrator:
    def __init__(self, df, config):
        self.df = df
        self.nrows = df.shape[0]
        self.ncols = df.shape[1]
        self.config = config
    
    def get_field(self, field):
        return self._get_series(field)

    def field_min(self, field):
        field_series = self._get_series(field)
        return field_series.min(axis=0)
    
    def field_max(self, field):
        field_series = self._get_series(field)
        return field_series.max(axis=0)

    def _get_series(self, field):
        return self.df[field]