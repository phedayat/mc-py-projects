from collections import Counter

from .data_wrapper import DataExctrator

class Operational(DataExctrator):
    def __init__(self, df, config):
        super().__init__(df, config)

    @property
    def duration(self):
        start = self.field_min("time")
        end = self.field_max("time")
        return end-start

    @property
    def expected_duration(self):
        ticks = self.config["ticks"]
        sleep_time = self.config["sleep_time"]
        return ticks*sleep_time

    @property
    def time_diffs(self):
        time = self.get_field("time")
        return [time[i+1]-time[i] for i in range(self.nrows-1)]
    
    @property
    def ops_times(self):
        sleep_time = self.config["sleep_time"]
        
        ops_times = []
        for i in self.time_diffs:
            ops_diff = i - sleep_time
            ops_times.append(ops_diff if ops_diff >= 0 else 0)
        return ops_times

    def avg_ops_time(self):
        ops_time_counts = Counter(self.ops_times)
        return sum(
            [
                k * ops_time_counts[k] 
                for k in ops_time_counts 
                if k != 0
            ]
        ) / self.nrows

    def summary(self):
        print(f"[      RUN_ID     ]\t{self.config['run_id']}")
        print(f"[EXPECTED_DURATION]\t{self.expected_duration}\tseconds")
        print(f"[     DURATION    ]\t{self.duration}\tseconds")
        print(f"[   AVG_OPS_TIME  ]\t{self.avg_ops_time()}\tseconds")