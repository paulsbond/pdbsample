import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import sklearn.linear_model


# TODO: Remove based on data completeness
# TODO: Remove if above linear model
# TODO: Remove if resolution is not close (or exact?) to reported


def cull():
    entries = os.listdir("entries")
    to_remove = set()

    resols = []
    rfrees = []
    for entry in entries:
        path = os.path.join("entries", entry, "refmac.xml")
        if not os.path.exists(path):
            # print(entry, "has no refmac.xml")
            to_remove.add(entry)
            continue
        xml = ET.parse(path).getroot()
        rfree = float(list(xml.iter("r_free"))[-1].text)
        resol = float(list(xml.iter("resolution_high"))[0].text)
        if rfree == -999:
            # print(entry, "did not produce a valid R-free")
            to_remove.add(entry)
            continue
        resols.append(resol)
        rfrees.append(rfree)

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
        print("Resolution", minres, "to", maxres, "90th R-free percentile:", tmp[-n])

    model = sklearn.linear_model.LinearRegression()
    x = np.array(percx).reshape((-1, 1))
    model.fit(x, percy)
    print("Linear Model")
    print("R2:", model.score(x, percy))
    print("Intercept:", model.intercept_)
    print("Slope:", model.coef_)
    slopex = np.arange(1, 3.5, 0.1)
    slopey = slopex * model.coef_ + model.intercept_

    plt.plot(resols, rfrees, "kx")
    plt.plot(percx, percy, "ro")
    plt.plot(slopex, slopey, "r-")
    plt.savefig("cull.png")
