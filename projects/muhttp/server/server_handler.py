import ujson

from time import sleep
from usocket import socket
from network import WLAN, STA_IF

from .request_handler import RequestHandler

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
    
    def serve(self):
        if not self.conn:
            return "Please open a socket"
        while True:
            sleep(1)
            client = self.conn.accept()[0]
            msg = client.recv(self.MAX_BYTES)
            print(msg)
            headers, data = self._process_message(msg)

            n_bytes = len(data)
            bytes_left = self._message_bytes_left(headers, n_bytes)
            if bytes_left > 0:
                temp_message = client.recv(bytes_left)
                _, temp_data = self._process_message(temp_message)
                data += temp_data

            print(headers)
            print(data)
            break