from time import sleep
from imu import MPU6050
from display import Display
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

disp = Display(sda=Pin(14), scl=Pin(15))
disp.send_to_display("Gyro XYZ:")

while True:
    # print(imu.accel.xyz)
    # print(imu.gyro.xyz)
    # print(imu.temperature)
    x = round(imu.gyro.x)
    y = round(imu.gyro.y)
    z = round(imu.gyro.z)
    with open("data.json", "a") as f:
        f.write(",".join(imu))
    disp.send_to_display(f"{x}, {y}, {z}", r=1)
    sleep(1)