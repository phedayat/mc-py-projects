from typing import Dict

class DataReader:
    pass

class DataWriter:
    def __init__(self, data: Dict[str, str]):
        self.data = data

    def write(self, file_path, headers):
        out = ",".join(map(lambda x: self.data[x], headers))+"\n"
        with open(file_path, "a") as f:
            f.write(out)