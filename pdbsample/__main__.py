#!/usr/bin/python3

from pdbsample.arguments import parse_arguments
from pdbsample.choose import choose
from pdbsample.refine import refine


def main():
    args = parse_arguments()
    if args.step == "choose":
        choose(args)
    if args.step == "refine":
        refine(args)


if __name__ == "__main__":
    main()
