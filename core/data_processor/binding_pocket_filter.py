"""
    Takes output of `binding_pocket_analyse` with
    RNA/Protein residue counts for various sphere sizes
    and filters given a min RNA concentration and distance cutoff.
"""
from collections import defaultdict
import pickle

def ligand_filter(name, kill):
    """
       Filter out ligands in kill list.

        Arguments:
            name (str): Name (ID) of ligand.
            kill (list): List of IDs that are invalid.
        Returns:
            bool: True if name is valid.
    """
    if name in kill:
        return False
    return True

def get_valids(lig_dict, max_dist, min_conc, min_size=4):
    """
        Filter ligand-pocket dictionary generated by `binding_pocket_analyze.py` by a given
        distance cutoff and RNA concentration.

        Arguments:
            lig_dict (dict): Dictionary keyed by pdbid with list of residue counts for each binding pocket.
            max_dist (int): Largest distance in Angstroms from ligand to RNA to allow for a binding site.
            min_conc (float): Minimum concentration of RNA to accept (num RNA residues / (num Protein + num RNA))
            min_size (int): Minimum number of RNA residues to allow in binding site. (default = 4)

        Returns:
            dict: Dictionary keyed by pbid with list of ligand redidue IDs that pass the tests.
    """
    ok_ligs = defaultdict(list)
    kill = ['IRI', 'UNL', 'UNX', 'XXX']
    unique_ligs = set()
    for pdb, ligands in lig_dict.items():
        for lig_id,lig_cuts in ligands:
            # lig_name = lig_id.split(":")[1]
            lig_name = lig_id.split(":")[2]
            #go over each distance cutoff
            for c in lig_cuts:
                tot = c['rna'] + c['protein']
                if tot == 0:
                    continue
                if c['rna'] < min_size:
                    continue
                rna_conc = c['rna'] / tot
                #scan until concentration is met and still under maximum distance.
                if (rna_conc >= min_conc and c['cutoff'] <= max_dist) and ligand_filter(lig_name, kill):
                    ok_ligs[pdb].append(lig_id)
                    print(lig_id)
                    unique_ligs.add(lig_name)
                    break
    print(f">>> Filtering ligands from {len(lig_dict)} PDBs.")
    print(f">>> minimum number of bases in pocket {min_size}")
    print(f">>> maximum distance from ligand {max_dist}")
    print(f">>> minimum RNA concentration {min_conc}")
    print(f">>> retained {len(ok_ligs)} PDBs")
    print(f">>> with a total of {sum(map(len,ok_ligs.values()))} binding sites")
    print(f">>> and {len(unique_ligs)} unique ligands.")
    print(f">>> passed ligands", unique_ligs)
    return ok_ligs

def ligs_to_txt(d, dest="../data/ligs.txt"):
    """
        Write selected ligands to text file for Chimera.
    """
    with open(dest, "w") as o:
        for pdb, ligs in d.items():
            o.write(" ".join([pdb, *ligs]) + "\n")
    pass
if __name__ == "__main__":
    d = pickle.load(open('lig_dict_mg.p', 'rb'))
    c = 10
    conc = .6
    ligs = get_valids(d, c, conc, min_size=4)
    pickle.dump(ligs, open("lig_dict_mg_filter.p", "wb"))
    # ligs_to_txt(ligs)
