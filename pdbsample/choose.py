from typing import List
import os
import random
import sys
import pdbsample.pdbe as pdbe


_CACHE_PATH = os.path.join("data", "chosen.txt")


class _ResolutionBin:
    def __init__(self, args, i):
        self.min_res = args.res_min + i * args.res_step
        self.max_res = args.res_min + (i + 1) * args.res_step
        self.entries = []
        self.chosen = []


def _assign_resolution_bins(args, entries):
    bins = [_ResolutionBin(args, i) for i in range(args.res_bins)]
    for entry in entries:
        if entry.resolution < args.res_min or entry.resolution > args.res_max:
            continue
        i = int((entry.resolution - args.res_min) / args.res_step)
        if i == len(bins):
            i -= 1
        bins[i].entries.append(entry)
    return bins


def _choose_new_entries(args) -> List[str]:
    print("Choosing a new set of entries")
    entries = pdbe.entries(args)
    res_bins = _assign_resolution_bins(args, entries)
    exclude = set()
    if args.exclude is not None:
        with open(args.exclude) as stream:
            exclude = {line.strip().lower() for line in stream}
    chosen_clusters = set()
    res_bins.sort(key=lambda res_bin: len(res_bin.entries))
    print("|-------------|---------|----------|--------|")
    print("| Resolution  | Entries | Filtered | Chosen |")
    print("|-------------|---------|----------|--------|")
    for res_bin in res_bins:
        res_bin.entries.sort(key=lambda entry: entry.quality, reverse=True)
        lower = int(len(res_bin.entries) * args.cut_best / 100)
        upper = int(len(res_bin.entries) * args.cut_worst / 100)
        filtered = res_bin.entries[lower:-upper]
        filtered = [e for e in filtered if e.pdbid not in exclude]
        random.shuffle(filtered)
        for entry in filtered:
            clusters = {entity.cluster for entity in entry.entities}
            if not chosen_clusters.intersection(clusters):
                res_bin.chosen.append(entry)
                chosen_clusters.update(clusters)
                if len(res_bin.chosen) == args.bin_entries:
                    break
        print(
            "| %4.2f - %4.2f | %7d | %8d | %6d |"
            % (
                res_bin.min_res,
                res_bin.max_res,
                len(res_bin.entries),
                len(filtered),
                len(res_bin.chosen),
            )
        )
    print("|-------------|---------|----------|--------|")
    return sorted(e.pdbid for r in res_bins for e in r.chosen)


def choose(args) -> None:
    chosen = _choose_new_entries(args)
    print("Writing chosen entries to", _CACHE_PATH)
    with open(_CACHE_PATH, "w") as stream:
        for pdbid in chosen:
            stream.write(pdbid + "\n")


def chosen() -> List[str]:
    print("Reading chosen entries from", _CACHE_PATH)
    if os.path.exists(_CACHE_PATH):
        with open(_CACHE_PATH) as stream:
            return [line.strip() for line in stream]
    sys.exit("Could not read chosen entries, run the choose step first")
