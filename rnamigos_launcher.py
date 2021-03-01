import os
import pickle

import networkx as nx

from nx2fp import *
from fp2lig import *


def launch(G, library_path, n_hits=30):
    run = 'ismb-tune_0'
    model, meta = load_model(run)
    fp_pred, _ = inference_on_graph(model, G, meta['edge_map'])

    if library_path is None:
        library = pickle.load(open(os.path.join("static", "libraries", "pdb_rna.p"), 'rb'))
    else:
        library = smiles_to_library(library_path)

    fp_pred = fp_pred.detach().numpy() > 0.5
    hits = screen(fp_pred, library, n_hits=n_hits)

    result_json = __results_to_json(hits, G, fp_pred);

    return result_json

def __results_to_json(hits, G, fp_pred):
    """
    Write launcher outputs as a single JSON object.
    """
    result_json = {}

    result_json['hits'] = hits
    result_json['graph'] = nx.node_link_data(G)
    result_json['fingerprint'] = list(fp_pred)

    return result_json

if __name__ == "__main__":
    launch("hi", None)
    pass