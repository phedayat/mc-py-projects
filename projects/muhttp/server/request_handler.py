class Request:
    def __init__(self, method, headers, data):
        self.method = method
        self.headers = headers
        self.data = data

class RequestHandler:
    def __init__(self, raw_request: bytes):
        self.raw_request = raw_request

    @property
    def request(self):
        return Request(*self._split_headers_data())

    def _get_raw_request_tokens(self):
        return list(
            filter(
                lambda x: x != "",
                map(
                    lambda x: x.strip(),
                    self.raw_request.decode("utf-8").split("\r")
                )
            )
        )

    def _split_headers_data(self):
        req = self._get_raw_request_tokens()
        data = req[-1]
        req_type = req[0]
        headers_pairs = req[1:-1]

        headers = dict()
        for pair in headers_pairs:
            header, value = list(map(lambda x: x.strip(), pair.split(":")))
            headers[header] = value
        return req_type, headers, data