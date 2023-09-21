import ujson

class ResponseHandler:
    def __init__(self, status, data, headers=dict()):
        self.headers = headers
        self.status = status
        self.data = ujson.dumps(data).encode("utf-8")
        self._create_headers()

    def _create_headers(self):
        self.headers["Content-Length"] = len(self.data)
        self.headers["Connection"] = "keep-alive"
        self.headers["Content-Type"] = "application/json"
    
    def get_start_line(self):
        return f"HTTP/1.1 {self.status}\n".encode("utf-8")

    def get_headers(self):
        header_string_lambda = lambda x: f"{x}: {self.headers[x]}\n".encode("utf-8")
        header_string = list(map(header_string_lambda, self.headers))
        header_string[-1] += "\n"
        return header_string
    
    def get_data(self):
        return self.data