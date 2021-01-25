#!/usr/bin/python3

from pdbsample.arguments import parse_arguments
from pdbsample.choose import choose
from pdbsample.refine import refine
from pdbsample.remove import remove


def main():
    args = parse_arguments()
    if args.step == "choose":
        choose(args)
    if args.step == "refine":
        refine(args)
    if args.step == "remove":
        remove()


if __name__ == "__main__":
    main()
