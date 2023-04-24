import sys
sys.path.append("/src")

from os import mount, VfsFat
from machine import Pin, SPI

from src.sdcard import SDCard

spi = SPI(
    0, # id, i.e. which SPI are we using
    baudrate=1000000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(0),
)

sd = SDCard(spi, Pin(1, Pin.OUT))
vfs = VfsFat(sd)
try:
    mount(vfs, "/sd")
except OSError:
    pass
