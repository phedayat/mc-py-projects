import os

from time import sleep
from src.imu import MPU6050
from machine import Pin, I2C

def remove_existing_data():
    try:
        os.remove("/data.csv")
    except OSError:
        pass

def create_data_directory():
    try:
        os.mkdir("/data")
    except FileExistsError:
        pass

if __name__=="__main__":
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    imu = MPU6050(i2c)
    
    remove_existing_data()
    create_data_directory()
    data_file = open("/data/data.csv", "a")
    headers = ','.join([
        'temp',
        'ax', 'ay', 'az',
        'gx', 'gy', 'gz'
    ])
    data_file.write(f"{headers}\n")
    while True:
        a = imu.accel.xyz
        g = imu.gyro.xyz
        obj = list(map(lambda x: str(x), [
            imu.temperature,
            a[0], a[1], a[2],
            g[0], g[1], g[2],
        ]))
        data_file.write(f"{','.join(obj)}\n")
        sleep(0.5)