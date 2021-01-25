import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "step",
        choices=["choose", "refine", "cull"],
        help="sampling step: either "
        "'choose' for choosing PDB entries, "
        "'refine' for refining them or "
        "'cull' to remove entries based on refinement data",
    )
    choose = parser.add_argument_group("choose step arguments")
    choose.add_argument(
        "--cut-best",
        type=float,
        default=5,
        metavar="X",
        help="percentage of best quality structures"
        "to remove from each bin (default: 5)",
    )
    choose.add_argument(
        "--cut-worst",
        type=float,
        default=50,
        metavar="X",
        help="percentage of worst quality structures"
        "to remove from each bin (default: 50)",
    )
    choose.add_argument(
        "--res-bins",
        type=int,
        default=10,
        metavar="N",
        help="number of resolution bins (default: 10)",
    )
    choose.add_argument(
        "--res-max",
        type=float,
        default=3.5,
        metavar="X",
        help="maximum resolution (exclusive) (default: 3.5)",
    )
    choose.add_argument(
        "--res-min",
        type=float,
        default=1.0,
        metavar="X",
        help="minimum resolution (inclusive) (default: 1.0)",
    )
    choose.add_argument(
        "--bin-entries",
        type=int,
        default=2,
        metavar="N",
        help="number of entries per resolution bin (default: 2)",
    )
    choose.add_argument(
        "--exclude",
        metavar="FILE",
        help="path to a file of PDB IDs to exclude, one per line",
    )
    args = parser.parse_args()
    args.res_step = (args.res_max - args.res_min) / args.res_bins
    return args
