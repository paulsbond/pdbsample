import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--res-bins",
        type=int,
        metavar="N",
        default=10,
        help="Number of resolution bins (default: 10)",
    )
    parser.add_argument(
        "--res-max",
        type=float,
        metavar="X",
        default=3.5,
        help="Maximum resolution (exclusive) (default: 3.5)",
    )
    parser.add_argument(
        "--res-min",
        type=float,
        metavar="X",
        default=1.0,
        help="Minimum resolution (inclusive) (default: 1.0)",
    )
    args = parser.parse_args()
    args.res_step = (args.res_max - args.res_min) / args.res_bins
    return args
