from machine import Pin
from time import sleep

class LedWrapper:
    def __init__(self) -> None:
        self.led = Pin(25, Pin.OUT)
    
    def on(self):
        self.led.value(1)
    
    def off(self):
        self.led.value(0)

    def blink(self, n):
        for _ in range(n):
            self.on()
            sleep(.5)
            self.off()

class ButtonWrapper:
    def __init__(self) -> None:
        self.button = Pin(15, Pin.IN, Pin.PULL_DOWN)

    def check_on(self):
        return not self.button.value()