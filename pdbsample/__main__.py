#!/usr/bin/python3

import random
import pdbsample.arguments as arguments
import pdbsample.pdbe as pdbe
import pdbsample.utils as utils


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


def choose_entries(entries):
    res_bins = assign_resolution_bins(entries)
    # chosen_clusters = set()
    res_bins.sort(key=lambda res_bin: len(res_bin.entries))
    for res_bin in res_bins:
        title = "Choosing %.2f-%.2fA structures (%d to choose from)" % (
            res_bin.min_res,
            res_bin.max_res,
            len(res_bin.structures),
        )
        print(title)
        # progress_bar = utils.ProgressBar(title, args.num_structures)
        # random.shuffle(res_bin.structures)
        # num_checked = 0
        # num_missing_files = 0
        # num_too_similar = 0
        # num_failed_validation = 0
        # for structure in res_bin.structures:
        #     passed = True
        #     num_checked += 1
        #     if not input_files_exist(structure):
        #         num_missing_files += 1
        #         passed = False
        #     clusters = {getattr(c, cluster_attr) for c in structure.chains.values()}
        #     if any(c in chosen_clusters for c in clusters):
        #         num_too_similar += 1
        #         passed = False
        #     if not validation_report_okay(structure):
        #         num_failed_validation += 1
        #         passed = False
        #     if passed:
        #         res_bin.chosen.append(models.Structure(structure))
        #         chosen_clusters.update(clusters)
        #         progress_bar.increment()
        #         if len(res_bin.chosen) == args.num_structures:
        #             break
        # progress_bar.finish()
        # print("Total number checked:          %6d" % num_checked)
        # print("Missing input files:           %6d" % num_missing_files)
        # print("Too similar to already chosen: %6d" % num_too_similar)
        # print("Failed validation checks:      %6d" % num_failed_validation)
        # print("")
    # return {s.id: s for r in res_bins for s in r.chosen}


def main():
    entries = pdbe.entries(ARGS)
    choose_entries(entries)


if __name__ == "__main__":
    ARGS = arguments.parse()
    main()
