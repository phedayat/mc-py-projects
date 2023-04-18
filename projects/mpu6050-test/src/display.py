from machine import I2C
from i2c_lcd import I2cLcd

class Display:
    def __init__(self, sda, scl):
        rows = 2
        cols = 16

        i2c = I2C(1, sda=sda, scl=scl, freq=100000)

        I2C_ADDR = 0x27
        self.lcd = I2cLcd(i2c, I2C_ADDR, rows, cols)
    
    def clear(self):
        self.lcd.clear()

    def send_to_display(self, message, r=0, c=0):
        self.lcd.move_to(c, r)
        self.lcd.putstr(message)