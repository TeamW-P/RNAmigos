import os
import pickle
import json

import networkx as nx

from .nx2fp import *
from .fp2lig import *
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import DrawingOptions                                      
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D  


def launch(G, library_path, n_hits=30):
    run = 'ismb-tune_0'
    model, meta = load_model(run)
    fp_pred, _ = inference_on_graph(model, G, meta['edge_map'])

    if library_path is None:
        with open(os.path.join("core", "static", "libraries", "pdb_rna.p"), 'rb') as f:
            library = pickle.load(f)
    else:
        library = smiles_to_library(library_path)

    fp_pred = fp_pred.detach().numpy() > 0.5
    hits = screen(fp_pred, library, n_hits=n_hits)
    hits_formatted = []
    for ligand in hits:
        i = 0
        hit = {}
        for smiles_data in ligand:
            if i % 2 == 0:
                smiles = smiles_data[0]
                smiles_svg = __draw(smiles)
                hit["smiles"] = smiles
                hit["smiles_svg"] = smiles_svg
            else:
                hit["score"] = smiles_data
            i += 1
        hits_formatted.append(hit)
    result_json = __results_to_json(hits_formatted, G, fp_pred.tolist());  

    return result_json

def __draw(smiles):
    m = Chem.MolFromSmiles(smiles)
    if m == None:
        print("Couldnt read SMILES")
        return
    mc = Chem.Mol(m.ToBinary())
    # try:
    if not mc.GetNumConformers():
        rdDepictor.Compute2DCoords(mc)
    drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])
    drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    svg = svg.replace(':svg','')
    svg = svg.replace('svg:','')
    return svg

def __results_to_json(hits, G, fp_pred):
    """
    Write launcher outputs as a single JSON object.
    """
    result_json = {}

    result_json['hits'] = hits
    result_json['graph'] = nx.node_link_data(G)
    result_json['fingerprint'] = json.dumps(fp_pred)

    return result_json

if __name__ == "__main__":
    launch("hi", None)
    pass