from os import mkdir
from json import dump
from time import sleep, time

class Run:
    def __init__(self, sd_prefix, config, mpu, led, off):
        self.config = config
        self.mpu = mpu
        self.led = led
        self.off = off

        self.continuous = self.config["ticks"] < 0

        self.id = self.config["run_id"]
        self.path = f"{sd_prefix}/{self.id}"
        self.data_path = f"{self.path}/{self.id}.csv"
        self.metadata_path = f"{self.path}/metadata.json"

    def init(self):
        self._init_run()

    def run(self):
        with open(self.data_path, "a") as f:
            i = 0
            self.led.on()
            while self.continuous or i < self.config["ticks"]:
                if self.off.check_on():
                    return
                self._run_unit(f, i)
                i += 1

    def _init_run(self):
        mkdir(self.path)
        with open(self.metadata_path, "w") as f:
            dump(self.config, f)
        with open(self.data_path, "w") as f:
            headers = ",".join(self.config["fields"])
            f.write(f"{headers}\n")

    def _run_unit(self, f, i):
        row = self._create_row(i)
        f.write(f"{row}\n")
        sleep(self.config["sleep_time"])

    def _create_row(self, i):
        a = self._get_accel()
        g = self._get_gyro()
        row = [i, time(), a[0], a[1], a[2], g[0], g[1], g[2]]
        return ",".join(map(str, row))

    def _get_accel(self):
        return self.mpu.driver.accel.xyz
    
    def _get_gyro(self):
        return self.mpu.driver.gyro.xyz
