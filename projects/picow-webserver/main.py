import ujson

from time import sleep
from usocket import socket
from network import WLAN, STA_IF

# Our own message processor 
# For raw HTTP 1.1 messages
def process_message(message):
    message_dict = {
        "Request": [],
    }
    message_split = list(map(lambda x: x.strip(), message.decode("utf-8").split("\r")))
    headers = message_split[:-1]
    body = message_split[-1]
    for i in headers:
        if i == "":
            continue
        key_value = list(map(lambda x: x.strip(), i.split(":")))
        if len(key_value) < 2:
            message_dict["Request"] += key_value
            continue
        message_dict[key_value[0]] = key_value[1]
    return message_dict, body

##### WIFI #####
def get_ssid_creds():
    with open("ssid.json") as config:
        return ujson.load(config)

def connect_wlan():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    creds = get_ssid_creds()
    wlan.connect(creds["SSID"], creds["SSID_PASSWORD"])
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected to {ip}!")
    return ip
##### END #####

##### Socket/Connections (Server) #####
# Create and open a socket (object)
def open_socket(ip):
	addr = (ip, 80)
	conn = socket()
	conn.bind(addr)
	conn.listen(1)
	return conn

# Serve/process data (HTML, JSON, plaintext, etc.) to
# a new connection
def serve(conn):
    i = 0
    while True:
        sleep(1) # just to allow for everything to prepare
        client = conn.accept()[0] # blocks until a connection arrives
        print(f"[{i}] Client connected: {client}")
        msg = client.recv(4096) # receive a message, max of 4096 bytes
        print(f"Message: {msg}")
        headers, data = process_message(msg)

        # Receive again if you didn't get the whole message
        n_bytes = len(data)
        if ("Content-Length" in headers and
            int(headers["Content-Length"]) > n_bytes):
            max_bytes = int(headers["Content-Length"])-n_bytes+1
            mtmp = client.recv(max_bytes)
            _, dtmp = process_message(mtmp)
            data = dtmp
        print(f'Data: {data}, {type(data)}, {data == ""}')
        print(f'Headers: {headers}')
        
        # Response data
        message = {
            "data": ujson.loads(data) if data != "" else None,
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }

        # Sending response headers
        client.send(b"HTTP/1.1 200 OK\n")
        client.send(b"Content-Type: application/json\n")
        client.send(b"Connection: keep-alive\n\n")
        
        # Sending response data
        client.sendall(ujson.dumps(message).encode("utf-8"))

        # Close the connection to the client
        client.close()
        i += 1
##### END #####

##### MAIN #####
if __name__=="__main__":
	try:
		ip = connect_wlan()
		conn = open_socket(ip)
		serve(conn)
	except KeyboardInterrupt:
		import sys
		conn.shutdown()
		conn.close()
		sleep(2)
		sys.exit(0)
##### END #####
