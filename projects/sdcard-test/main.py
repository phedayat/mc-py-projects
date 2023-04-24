try:
    data_path = "/sd/data"

    with open(data_path, "a") as f:
        f.write("Hello world!\n")
        
    with open(data_path) as f:
        print(f.readlines())
except:
    from time import sleep
    for _ in range(100):
        print("No directory /sd")
        sleep(1)