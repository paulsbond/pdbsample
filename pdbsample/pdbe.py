import json
import os
import sys
import requests
import solrq


def _query(min_res, max_res, min_length):
    return solrq.Q(
        experimental_method="X-ray diffraction",
        experiment_data_available="y",
        resolution=solrq.Range(min_res, max_res),
        molecule_type="Protein",
        max_observed_residues=solrq.Range(min_length, solrq.ANY),
        seq_30_cluster_number=solrq.Range(solrq.ANY, solrq.ANY),
    )


def _pdbe_docs(min_res, max_res, min_length):
    path = os.path.join("data", "pdbe.json")
    if os.path.exists(path):
        print("Using cached PDBe data")
        with open(path) as stream:
            return json.load(stream)
    print("Making a new query to PDBe")
    request_url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?"
    filter_list = "pdb_id,resolution,overall_quality,chain_id,seq_30_cluster_number"
    query = _query(min_res, max_res, min_length)
    request_data = {"fl": filter_list, "q": query, "rows": 10000, "wt": "json"}
    response = requests.post(request_url, data=request_data)
    if response.status_code == 200:
        response_data = response.json().get("response", {})
        print("Entries found:", response_data["numFound"])
        os.makedirs("data", exist_ok=True)
        with open("data/pdbe.json", "w") as stream:
            json.dump(response_data["docs"], stream, separators=(",", ":"))
        return response_data["docs"]
    print(f"Response with status code {response.status_code} received")
    sys.exit(response.text)


class _Entry:
    def __init__(self, doc):
        self.pdbid = doc["pdb_id"]
        self.quality = doc["overall_quality"]
        self.resolution = doc["resolution"]
        self.entities = []


class _Entity:
    def __init__(self, doc):
        self.chain = doc["chain_id"][0]
        self.cluster = doc["seq_30_cluster_number"]


def entries(min_res=1.0, max_res=3.5, min_length=50):
    entry_dict = {}
    docs = _pdbe_docs(min_res, max_res, min_length)
    docs.sort(key=lambda d: d["pdb_id"])
    for doc in docs:
        pdbid = doc["pdb_id"]
        entry = entry_dict.setdefault(pdbid, _Entry(doc))
        assert entry.resolution == doc["resolution"]
        assert entry.quality == doc["overall_quality"]
        entry.entities.append(_Entity(doc))
    return list(entry_dict.values())
