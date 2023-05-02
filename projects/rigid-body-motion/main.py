import json

from os import mkdir
from sys import exit
from machine import Pin, I2C
from time import sleep, time

from src.config import Config
from src.drivers.imu import MPU6050
from src.mpu_wrapper import MpuWrapper

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
    return ",".join(map(lambda x: str(x), row))

def run_unit(i, imu_dev, file, sleep_time):
    row = create_entry(i, imu_dev)
    file.write(f"{row}\n")
    sleep(sleep_time)

if __name__=="__main__":
    try:
        # Configure and prepare the MPU
        mpu = MpuWrapper()

        # Configure and prepare the run
        config = Config()
        run = Run(config, mpu.unit) # [TODO]
        
        # [TODO]
        # Get run directory and data paths (on SD)
        run_path = run.path
        run_csv_path = run.data_path

        run_path = init_run(config)
        run_csv_path = build_run_csv_path(run_path, config["run_id"])

        led = LedWrapper() # [TODO]
        off_buttton = ButtonWrapper() # [TODO]

        # Begin the run
        led = Pin(25, Pin.OUT)
        off_button = Pin(15, Pin.IN, Pin.PULL_DOWN)

        sleep_time = config["sleep_time"]
        ticks = config["ticks"]

        with open(run_csv_path, "a") as f:
            led.value(1)
            infty = ticks < 0
            infty = run.continuous # [TODO]
            i = 0
            while infty or i < ticks:
                if not off_button.value():
                    break
                run_unit(i, mpu.driver, f, sleep_time)
                i += 1
    except KeyboardInterrupt:
        print("SIGINT")
    finally:
        led.value(0)
        exit(0)
