import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cut-best-quality",
        type=float,
        default=5,
        help="Percentage of best quality structures to remove from each bin (default: 5)",
    )
    parser.add_argument(
        "--cut-worst-quality",
        type=float,
        default=25,
        help="Percentage of worst quality structures to remove from each bin (default: 25)",
    )
    parser.add_argument(
        "--res-bins",
        type=int,
        default=10,
        help="Number of resolution bins (default: 10)",
    )
    parser.add_argument(
        "--res-max",
        type=float,
        default=3.5,
        help="Maximum resolution (exclusive) (default: 3.5)",
    )
    parser.add_argument(
        "--res-min",
        type=float,
        default=1.0,
        help="Minimum resolution (inclusive) (default: 1.0)",
    )
    parser.add_argument(
        "--bin-entries",
        type=int,
        default=2,
        help="Number of entries per resolution bin (default: 2)",
    )
    args = parser.parse_args()
    args.res_step = (args.res_max - args.res_min) / args.res_bins
    return args
