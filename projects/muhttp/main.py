from server.server_handler import Server



if __name__=="__main__":
    server = Server(config_path="./config.json")
    server.open_socket(
        port=80,
        max_requests=1,
    )
    server.serve({
        "/": lambda x, y: "Hello",
        "/app": lambda x, y: "Unlocked a new route!",
        "/dev": lambda x, y: {"input": y},
    })