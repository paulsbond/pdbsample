#!/usr/bin/python3

import pdbsample.arguments as arguments
import pdbsample.choose as choose


def main():
    args = arguments.parse()
    chosen = choose.choose_entries(args)
    print(chosen)


if __name__ == "__main__":
    main()
