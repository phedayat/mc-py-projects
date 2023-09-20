from server.server_handler import Server

if __name__=="__main__":
    server = Server(config_path="./config.json")
    server.open_socket()
    server.serve()