#!/usr/bin/python3

import pdbsample.arguments as arguments
import pdbsample.pdbe as pdbe
import pdbsample.choose as choose


def main():
    args = arguments.parse()
    entries = pdbe.entries(args)
    chosen = choose.choose_entries(args, entries)
    print(chosen)


if __name__ == "__main__":
    main()
