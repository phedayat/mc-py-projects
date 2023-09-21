import ujson

from utime import sleep
from usocket import socket
from network import WLAN, STA_IF

from .request_handler import RequestHandler
from .response_handler import ResponseHandler

class WifiHandler:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def _get_ssid_creds(self):
        with open(self.config_path) as config_file:
            config = ujson.load(config_file)
            ssid = config["SSID"]
            password = config["SSID_PASSWORD"]
            return [ssid, password]
    
    def _connect_wlan(self):
        wlan = WLAN(STA_IF)
        wlan.active(True)
        creds = self._get_ssid_creds()
        wlan.connect(*creds)
        while not wlan.isconnected():
            print("Waiting for connection...")
            sleep(1)
        ip = wlan.ifconfig()[0]
        print(f"Connected to {ip}")
        return ip
    
    def connect(self):
        return self._connect_wlan()


class Server:
    MAX_BYTES = 4096

    def __init__(self, config_path: str) -> None:
        self.wifi = WifiHandler(config_path=config_path)
        self.ip = self.wifi.connect()
        self.conn = None

    def open_socket(self, port=80, max_requests=1):
        addr = (self.ip, port)
        conn = socket()
        conn.bind(addr)
        conn.listen(max_requests)
        self.conn = conn
    
    def _send_response(self, client, start_line, headers, data):
        client.send(start_line)
        for header in headers:
            client.send(header)
        client.sendall(data)

    def serve(self, routes):
        if not self.conn:
            raise ValueError("No socket open")
        while True:
            sleep(1)
            client = self.conn.accept()[0]
            msg = client.recv(self.MAX_BYTES)
            
            req_handler = RequestHandler(msg)

            while req_handler.unfinished_data:
                msg = client.recv(self.MAX_BYTES)
                req_handler.add_missing_data(msg)

            req = req_handler.get_request()
            if req.route not in routes:
                # return a response
                return "Route does not exist"
            data = routes[req.route](req.method, req.data)
            res_handler = ResponseHandler("200 OK", {"result": data})
            self._send_response(
                client, res_handler.get_start_line(),
                res_handler.get_headers(), res_handler.get_data()
            )
            client.close()