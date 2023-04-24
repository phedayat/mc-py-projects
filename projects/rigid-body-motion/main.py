from time import sleep
from src.imu import MPU6050
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c)

sd_path = "/sd"

with open(f"{sd_path}/data.txt", "a") as f:
    i = 0
    while True:
        row = [i, mpu.accel.x, mpu.accel.y, mpu.accel.z]
        f.write(f"{row}\n")
        i += 1
        sleep(1)