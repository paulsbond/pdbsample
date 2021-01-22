#!/usr/bin/python3

import arguments
import pdbe


class ResolutionBin:
    def __init__(self, i):
        self.min_res = ARGS.res_min + i * ARGS.res_step
        self.max_res = ARGS.res_min + (i + 1) * ARGS.res_step
        self.entries = []
        self.chosen = []


def assign_resolution_bins(entries):
    bins = [ResolutionBin(i) for i in range(ARGS.res_bins)]
    for entry in entries:
        if entry.resolution < ARGS.res_min or entry.resolution > ARGS.res_max:
            continue
        i = int((entry.resolution - ARGS.res_min) / ARGS.res_step)
        if i == len(bins):
            i -= 1
        bins[i].entries.append(entry)
    return bins


def main():
    entries = pdbe.entries(ARGS)
    res_bins = assign_resolution_bins(entries)
    for res_bin in res_bins:
        print(res_bin.min_res, res_bin.max_res, len(res_bin.entries))


if __name__ == "__main__":
    ARGS = arguments.parse()
    main()
