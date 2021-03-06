from typing import List
import json
import os
import sys
import requests
import solrq


_CACHE_PATH = os.path.join("data", "pdbe.json")


def _query(min_res: float, max_res: float) -> solrq.Q:
    return solrq.Q(
        experimental_method="X-ray diffraction",
        experiment_data_available="y",
        resolution=solrq.Range(min_res, max_res),
        molecule_type="Protein",
        max_observed_residues=solrq.Range(50, solrq.ANY),
        seq_30_cluster_number=solrq.Range(solrq.ANY, solrq.ANY),
    )


def _pdbe_docs(min_res: float, max_res: float) -> List[dict]:
    if os.path.exists(_CACHE_PATH):
        print("Using cached PDBe data")
        with open(_CACHE_PATH) as stream:
            return json.load(stream)
    print("Making a new query to PDBe")
    request_url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?"
    filter_list = "pdb_id,resolution,overall_quality,chain_id,seq_30_cluster_number"
    query = _query(min_res, max_res)
    request_data = {"fl": filter_list, "q": query, "rows": 1000000, "wt": "json"}
    response = requests.post(request_url, data=request_data)
    if response.status_code == 200:
        response_data = response.json().get("response", {})
        print("Entries found:", response_data["numFound"])
        os.makedirs("data", exist_ok=True)
        with open(_CACHE_PATH, "w") as stream:
            json.dump(response_data["docs"], stream, separators=(",", ":"))
        return response_data["docs"]
    print(f"Response with status code {response.status_code} received")
    sys.exit(response.text)


class _Entry:
    def __init__(self, doc: dict):
        self.pdbid = doc["pdb_id"]
        self.quality = doc["overall_quality"]
        self.resolution = doc["resolution"]
        self.entities = []


class _Entity:
    def __init__(self, doc: dict):
        self.chain = doc["chain_id"][0]
        self.cluster = doc["seq_30_cluster_number"]


def entries(args) -> List[_Entry]:
    entry_dict = {}
    docs = _pdbe_docs(args.res_min, args.res_max)
    docs.sort(key=lambda d: d["pdb_id"])
    for doc in docs:
        pdbid = doc["pdb_id"]
        entry = entry_dict.setdefault(pdbid, _Entry(doc))
        assert entry.resolution == doc["resolution"]
        assert entry.quality == doc["overall_quality"]
        entry.entities.append(_Entity(doc))
    return list(entry_dict.values())
