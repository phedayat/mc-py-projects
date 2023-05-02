import sys
sys.path.append("/src")

from os import mount
from machine import Pin

from src.sd_spi_wrapper import SdSpiWrapper

sck = Pin(2)
mosi = Pin(3)
miso = Pin(0)
cs = Pin(1, Pin.OUT)
sd = SdSpiWrapper(0, sck, mosi, miso, cs)

try:
    mount(sd.vfs, "/sd")
except OSError:
    pass
import sys
sys.path.append("/src")

from os import mount
from machine import Pin

from src.SdSpiWrapper import SdSpiWrapper

sck = Pin(2)
mosi = Pin(3)
miso = Pin(0)
cs = Pin(1, Pin.OUT)
sd = SdSpiWrapper(0, sck, mosi, miso, cs)

try:
    mount(sd.vfs, "/sd")
except OSError:
    pass
