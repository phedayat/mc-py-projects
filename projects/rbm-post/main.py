from collections import Counter
from argparse import ArgumentParser

from src.runs import RunObject
from src.data_wrapper import DataExctrator

ARGS = [
    "--run-id",
]

def get_args():
    parser = ArgumentParser(prog="RBM Post Processing")
    [parser.add_argument(arg) for arg in ARGS]
    return parser.parse_args()

if __name__=="__main__":
    args = get_args()

    run = RunObject(args.run_id)
    info = DataExctrator(run.data.df, run.config)

    info.summary()
