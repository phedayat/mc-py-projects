from time import sleep_ms
from i2c_lcd import I2cLcd
from lcd_api import LcdApi
from machine import Pin, ADC, I2C

def read_temp(adc):
    adc_v = adc.read_u16() * (3.3 / 65535)
    t_c = 27 - (adc_v - .706)/.001721
    t_f = 32 + (1.8*t_c)
    return {"C": t_c, "F": t_f}

class Display:
    def __init__(self):
        rows = 2
        cols = 16

        sdaPin = Pin(14)
        sclPin = Pin(15)

        i2c = I2C(1, sda=sdaPin, scl=sclPin, freq=100000)

        I2C_ADDR = 0x27
        self.lcd = I2cLcd(i2c, I2C_ADDR, rows, cols)
    
    def clear(self):
        self.lcd.clear()

    def send_to_display(self, message, r=0, c=0):
        self.lcd.move_to(c, r)
        self.lcd.putstr(message)

# @staticmethod
# def find_displays():
#   i2c.scan() and more
# addr = Display.find_displays()[0]
# display = Display(rows, cols, sdaPin, sclPin, i2c_num, i2c_addr)
display = Display()

display.clear()
display.lcd.hal_backlight_on()
display.send_to_display("Temperature:")
display.send_to_display("F", 1, 15)

sleep_ms(2000)

adc = machine.ADC(4)

prev = None
while True:
    try:
        temp = read_temp(adc)
        stemp = f"{temp['F']:.2f}"
        if prev and prev == stemp:
            sleep_ms(1500)
            continue
        else:
            prev = stemp
        display.send_to_display(stemp, 1, 0)
        sleep_ms(1500)
    except KeyboardInterrupt:
        display.lcd.hal_backlight_off()
        import sys
        sys.exit(0)
