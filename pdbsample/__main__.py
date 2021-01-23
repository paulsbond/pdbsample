#!/usr/bin/python3

import pdbsample.arguments as arguments
import pdbsample.choose as choose


def main():
    args = arguments.parse()
    choose.choose_entries(args)


if __name__ == "__main__":
    main()
