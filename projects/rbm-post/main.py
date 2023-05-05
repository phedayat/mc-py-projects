from argparse import ArgumentParser

from src.runs import RunObject
from src.operational import Operational

ARGS = [
    "--run-id",
]

def get_args():
    parser = ArgumentParser(prog="Rigid Body Motion Data Processing")
    [parser.add_argument(arg) for arg in ARGS]
    return parser.parse_args()

if __name__=="__main__":
    args = get_args()

    run = RunObject(args.run_id)
    ops_info = Operational(run.data.df, run.config)

    ops_info.summary()
