import collections
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import sklearn.linear_model
import pdbsample.pdbe as pdbe


class _Result:
    def __init__(self, path: str):
        xml = ET.parse(path).getroot()
        self.rfree = float(list(xml.iter("r_free"))[-1].text)
        self.resolution = float(list(xml.iter("resolution_high"))[-1].text)
        self.completeness = float(list(xml.iter("data_completeness"))[-1].text)


def _print_reasons(to_remove: dict):
    print("Removed", len(to_remove), "entries for the following reasons:")
    reason_counter = collections.Counter(to_remove.values())
    for reason, count in reason_counter.most_common():
        print(reason, f"({count})")


def _write_reasons_to_file(to_remove: dict):
    path = os.path.join("data", "removed.txt")
    with open(path, "w") as stream:
        for entry in sorted(to_remove.keys()):
            reason = to_remove[entry]
            stream.write(f"{entry} {reason}\n")


def _rfree_outliers(results: dict):
    resols = [result.resolution for result in results.values()]
    rfrees = [result.rfree for result in results.values()]

    percx = []
    percy = []
    for res in np.arange(1, 3.1, 0.1):
        minres = res
        maxres = res + 0.5
        tmp = [
            rfree
            for resol, rfree in zip(resols, rfrees)
            if resol >= minres and resol <= maxres
        ]
        tmp.sort()
        n = int(len(tmp) * 0.10)
        percx.append((minres + maxres) / 2)
        percy.append(tmp[-n])
        print(
            f"Resolution {minres:.1f} to {maxres:.1f} 90th R-free percentile: {tmp[-n]:.3}"
        )

    model = sklearn.linear_model.LinearRegression()
    x = np.array(percx).reshape((-1, 1))
    model.fit(x, percy)
    print("Linear Model")
    print("R2:", model.score(x, percy))
    print("Intercept:", model.intercept_)
    print("Slope:", model.coef_)
    with open(os.path.join("data", "cutoff.txt"), "w") as stream:
        stream.write(f"{model.coef_} * resolution + {model.intercept_}")

    slopex = np.arange(1, 3.5, 0.1)
    slopey = slopex * model.coef_ + model.intercept_

    plt.plot(resols, rfrees, "kx")
    plt.plot(percx, percy, "ro")
    plt.plot(slopex, slopey, "r-")
    plt.savefig(os.path.join("data", "cutoff.png"))

    for entry, result in results.items():
        cutoff = result.resolution * model.coef_ + model.intercept_
        if result.rfree > cutoff:
            yield entry


def remove(args):
    pdbe_resolution = {e.pdbid: e.resolution for e in pdbe.entries(args)}
    entries = sorted(os.listdir("entries"))
    to_remove = {}
    results = {}
    for entry in entries:
        xml_path = os.path.join("entries", entry, "refmac.xml")
        if not os.path.exists(xml_path):
            to_remove[entry] = "Refmac XML does not exist"
            continue
        result = _Result(xml_path)
        if result.rfree == -999:
            to_remove[entry] = "R-free value of -999"
            continue
        if result.completeness < 90:
            to_remove[entry] = "Data completeness below 90%"
            continue
        if round(result.resolution, 2) != round(pdbe_resolution[entry], 2):
            to_remove[entry] = "Reported resolution different to refinement resolution"
            continue
        results[entry] = result
    for entry in _rfree_outliers(results):
        to_remove[entry] = "High R-free value for the resolution"
    _print_reasons(to_remove)
    _write_reasons_to_file(to_remove)
    os.makedirs("removed", exist_ok=True)
    for entry in to_remove:
        src = os.path.join("entries", entry)
        dst = os.path.join("removed", entry)
        os.rename(src, dst)
