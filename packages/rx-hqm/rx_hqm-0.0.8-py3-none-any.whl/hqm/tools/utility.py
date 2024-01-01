import os
import json
import uproot
import pickle


def get_project_root() -> str:
    return os.environ['HQMDIR'] + '/' 

def dump_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)


def load_json(path):
    with open(path, "r") as f:
        obj = json.load(f)
    return obj


def dump_pickle(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def read_root(path, tree_name):
    # read root file and return awkward array
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} is not found.")

    with uproot.open(path) as f:
        events = f[tree_name]
        data_array = events.arrays()
    return data_array
