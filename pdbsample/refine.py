import distutils.spawn
import multiprocessing
import os
import subprocess
import sys
import time
import urllib.request
from pdbsample.choose import chosen


LOCK = multiprocessing.Lock()


def _lock(seconds: int = 1) -> None:
    LOCK.acquire()
    time.sleep(seconds)
    LOCK.release()


def _download(filename: str) -> None:
    if not os.path.exists(filename):
        url = "https://www.ebi.ac.uk/pdbe/entry-files/download/" + filename
        urllib.request.urlretrieve(url, filename)


def _gemmi(entry: str) -> None:
    if not os.path.exists(f"r{entry}sf.mtz"):
        subprocess.call(["gemmi", "cif2mtz", f"r{entry}sf.ent", f"r{entry}sf.mtz"])


def _refmac(entry: str) -> None:
    if not os.path.exists("refmac.log"):
        arguments = [
            "refmac5",
            "HKLIN", f"./r{entry}sf.mtz",
            "XYZIN", f"./{entry}.cif",
            "HKLOUT", "./refmac.mtz",
            "XMLOUT", "./refmac.xml",
            "XYZOUT", "./refmac.cif",
        ]
        with open("refmac.log", "w") as log_stream:
            with open("refmac.err", "w") as err_stream:
                process = subprocess.Popen(
                    args=arguments,
                    stdin=subprocess.PIPE,
                    stdout=log_stream,
                    stderr=err_stream,
                    encoding="utf8",
                )
                process.stdin.write("NCYCLES 10\n")
                process.stdin.write("MAKE NEWLIGAND NOEXIT\n")
                process.stdin.write("PHOUT\n")
                process.stdin.write("END\n")
                process.stdin.close()
                process.wait()


def _refine_entry(entry: str) -> None:
    _lock()
    directory = os.path.join("entries", entry)
    os.makedirs(directory, exist_ok=True)
    os.chdir(directory)
    _download(f"r{entry}sf.ent")
    _download(f"{entry}.cif")
    _gemmi(entry)
    _refmac(entry)
    os.chdir(os.path.join("..", ".."))


def refine(args) -> None:
    for program in ("gemmi", "refmac5"):
        if not distutils.spawn.find_executable(program):
            sys.exit(f"Cannot find {program} executable")
    entries = chosen()
    processes = os.cpu_count() or 1
    print("Refining", len(entries), "entries using", processes, "processes")
    pool = multiprocessing.Pool(processes)
    pool.map(_refine_entry, entries)
