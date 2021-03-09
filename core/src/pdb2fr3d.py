"""
    Take user's PDB and convert it to FR3D graph (networkx)
"""

import os
import subprocess
import itertools

import networkx as nx
from Bio.PDB import *

FR3D_SCRIPT = "/home/flask/carnaval.git/Src/FR3D_Minimal"
faces = ['W', 'S', 'H']
orientations = ['C', 'T']
VALID_EDGES = set(['B53'] + [orient + "".join(e1 + e2) for e1, e2 in itertools.product(faces, faces) for orient in orientations])


def parse_fr3d(fr3d_path, pdb_path):
    """
        Parse fr3d annotations and return a graph.

        Sample line:
        "1_A_17_G","s53","1_A_16_G"

    """
    G = nx.Graph()
    nucs = {}

    with open(fr3d_path, "r") as fr3d:
        for line in fr3d:
            base_1, label, base_2 = line.split(",")
            chain_1, pos_1, nuc_1 = base_1.split("_")[1:]
            chain_2, pos_2, nuc_2 = base_2.split("_")[1:]
            label = label.upper().strip()[1:-1]
            if label in VALID_EDGES:
                label = label[0] + "".join(sorted(label[1:]))
                G.add_edge((chain_1, pos_1), (chain_2, pos_2), label=label)
                nucs[(chain_1, str(pos_1))] = nuc_1[0].strip()
                nucs[(chain_2, str(pos_2))] = nuc_2[0].strip()
    nx.set_node_attributes(G, nucs, 'nuc')

    # use BioPython to fill in the backbones
    parser = MMCIFParser(QUIET=True)
    struc = parser.get_structure('', pdb_path)[0]
    for chain in struc:
        reslist = list(chain)
        for i,residue in enumerate(reslist):
            if i == 0:
                continue
            r1 = (chain.id, str(residue.id[1]))
            r2 = (chain.id, str(reslist[i-1].id[1]))
            print(r1, r2)
            try:
                G[r1]
                G[r2]
            except:
                continue
            else:
                G.add_edge(r1, r2, label='B53')
    return G

def get_fr3d(pdb_path):
    #call MATLAB
    cwd = os.getcwd()
    os.chdir(FR3D_SCRIPT)

    pdb_folder, filename = os.path.split(pdb_path)
    dest = os.path.join(pdb_folder, filename.replace(".cif", ".csv"))
    print(f"pdb {pdb_folder}, {filename}, {dest}")
    matlab_cmd = f"setup_path; addpath '{pdb_folder}';annotate_pdb('{filename}', '{dest}');quit"
    try:
        subprocess.run(["matlab",
                       "-nodisplay",
                       "-r",
                       matlab_cmd])
    except Exception as e:
        print(e)
    else:
        return dest
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    parse_fr3d("1aju.csv", "")
    pass
