""" Take predicted ligand and return drawing + database hits. """

from functools import partial
import pickle

import numpy as np
from scipy.spatial.distance import jaccard

molSize=(250,100)

def screen(fp_pred, library, n_hits=30):
    """
        Find closest molecules to predition in library.
        Returns list [(smiles, fingerprint, distance), ... ()]
    """
    jaccard_partial = partial(jaccard, fp_pred)
    distances = map(jaccard_partial, (f[1] for f in library.items()))
    lib_dists = zip(library.items(), distances)
    hits = sorted(lib_dists, key=lambda x:x[1])[:n_hits]
    return hits

def smiles_to_library(smiles_file):
    library = {}
    with open(smiles_file, "r") as smiles:
        for l in smiles:
            try:
                smile = l.split()[0].strip()
                mol = pybel.readstring('smi', smile)
                fp = mol.calcfp('maccs').bits
                fp = index_to_vec(fp, nbits=166)
                library[smile] = fp
            except Exception as e:
                print(e)
                continue
    return library

def index_to_vec(fp, nbits=1024):
    """
    Convert list of 1 indices to numpy binary vector.

    Returns:
        `array`: 1x1024 binary numpy vector
    """
    # vec = np.zeros(166)
    vec = np.zeros(nbits)
    vec[fp] = 1
    return vec

if __name__ == "__main__":
    lib = smiles_to_library("static/libraries/pdb_rna_smiles.txt")
    pickle.dump(lib, open("static/libraries/pdb_rna.p", "wb"))
    pass
