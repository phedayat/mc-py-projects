import ujson

class Request:
    def __init__(self, start_line, headers, data):
        self.method, self.route, self.http_version = self._split_start_line(start_line)
        self.headers = headers
        self.data = data

    def _split_start_line(self, start_line):
        return list(map(lambda x: x.strip(), start_line.split(" ")))

class RequestHandler:
    def __init__(self, raw_request: bytes):
        self.start_line, self.headers, self.data = self._split_request(raw_request)
        self.unfinished_data = False
        if self._check_data() > 0:
            self.unfinished_data = True

    def get_request(self):
        return Request(
            start_line=self.start_line,
            headers=self.headers,
            data=ujson.loads(self.data),
        )

    def add_missing_data(self, raw_request):
        _, _, data = self._split_request(raw_request)
        self.data += data
        if self._check_data() == 0:
            self.unfinished_data = False

    def _message_bytes_left(self, headers, data_len):
        key = "Content-Length"
        if (key in headers and
            int(headers[key]) > data_len):
            return int(headers[key])-data_len
        return 0

    def _check_data(self):
        bytes_left = len(self.data)
        return self._message_bytes_left(self.headers, bytes_left)

    def _get_raw_request_tokens(self, raw_req):
        return list(
            filter(
                lambda x: x != "",
                map(
                    lambda x: x.strip(),
                    raw_req.decode("utf-8").split("\r")
                )
            )
        )

    def _split_request(self, raw_req):
        req = self._get_raw_request_tokens(raw_req)
        data = req[-1]
        start_line = req[0]
        headers_pairs = req[1:-1]

        headers = dict()
        for pair in headers_pairs:
            header, value = list(map(lambda x: x.strip(), pair.split(":")))
            headers[header] = value
        return start_line, headers, data