from machine import Pin
from time import sleep_ms

class TestClass:
	def __init__(self, pin_number):
		self.pin = Pin(pin_number, Pin.OUT)
	
	def blink(self, n):
		for _ in range(n):
			self.pin.toggle()
			sleep_ms(500)
			self.pin.toggle()
			sleep_ms(500)
			
