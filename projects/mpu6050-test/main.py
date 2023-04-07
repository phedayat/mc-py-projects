from time import sleep
from imu import MPU6050
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

while True:
    print(imu.accel.xyz)
    print(imu.gyro.xyz)
    print(imu.temperature)
    sleep(0.5)