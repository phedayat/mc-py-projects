import json

from os import mkdir
from src.imu import MPU6050
from machine import Pin, I2C
from time import sleep, time

def get_config():
    with open("/config.json") as f:
        config = json.load(f)
        return config

def init_run(metadata):
    run_id = metadata["run_id"]
    run_path = f"/sd/{run_id}"
    mkdir(run_path)
    with open(f"{run_path}/metadata.json", "a") as metadata_file:
        json.dump(metadata, metadata_file)
    with open(f"{run_path}/{run_id}.csv", "w") as f:
        headers = ",".join(metadata["fields"])
        f.write(f"{headers}\n")
    return run_path

def build_run_csv_path(run_path, run_id):
    return f"{run_path}/{run_id}.csv"

def get_accel_list(imu_dev):
    return imu_dev.accel.xyz

def get_gyro_list(imu_dev):
    return imu_dev.gyro.xyz

def create_entry(i, imu_dev):
    accel = get_accel_list(imu_dev)
    gyro = get_gyro_list(imu_dev)
    row = [i, time(), accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2]]
    return ",".join(row)

if __name__=="__main__":
    # Prepare MPU6050 driver
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
    mpu = MPU6050(i2c)

    # Configure and prepare the run
    metadata = {
        "run_id": "test_run_2",
        "fields": ["index", "time", "ax", "ay", "az", "gx", "gy", "gz"],
    }
    run_path = init_run(metadata["run_id"], metadata)
    run_csv_path = build_run_csv_path(run_path, metadata["run_id"])

    # Begin the run
    led = Pin(25, Pin.OUT)
    with open(run_csv_path, "a") as f:
        i = 0
        led.value(1)
        while True:
            row = create_entry(i, mpu)
            f.write(f"{row}\n")
            i += 1
            sleep(1.5)
