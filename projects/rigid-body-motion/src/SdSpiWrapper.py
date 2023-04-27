from os import VfsFat
from machine import SPI

from src.drivers.sdcard import SDCard

class SdSpiWrapper:
    def __init__(self, spi_id, sck, mosi, miso, cs):
        self.spi = SPI(
            spi_id,
            baudrate=1000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB,
            sck=sck,
            mosi=mosi,
            miso=miso,
        )
        self.sd = SDCard(self.spi, cs)
        self.vfs = VfsFat(self.sd)
