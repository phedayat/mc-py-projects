from machine import I2C, Pin
from .drivers.imu import MPU6050

class MpuWrapper:
    I2C_ID = 0
    SDA = 4
    SCL = 5
    FREQ = 400_000

    def __init__(self):
        self.sda = Pin(self.SDA)
        self.scl = Pin(self.SCL)
        
        self.i2c = I2C(
            self.I2C_ID, 
            sda=self.sda, 
            scl=self.scl, 
            freq=self.FREQ
        )
        self.driver = MPU6050(self.i2c)
    