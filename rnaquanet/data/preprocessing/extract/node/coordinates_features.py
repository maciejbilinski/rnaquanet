import numpy as np
import pandas as pd

from Bio.PDB.PDBParser import PDBParser
from rnaquanet.utils.custom_types import PathType
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig

def extract_coordinates(config: RnaquanetConfig, filtered_pdb_file_path: PathType):
    """
    Extract coordinates of nucleotides from filtered pdb file.

    Args:
    - filtered_pdb_file_path - absolute path to filtered pdb file
    - config - Config file

    Returns:
    - Pandas dataframe with basepair node features
    """
    structure = PDBParser(PERMISSIVE=1, QUIET=True).get_structure(
        "str", str(filtered_pdb_file_path))[0]
    x=[]
    y=[]
    z=[]
    found=False
    for chain in structure:
        for residue in chain:
            found=False
            for atom in residue:
                if atom.name==config.data.features.atom_for_distance_calculations:
                    coord = atom.get_coord()
                    x.append(coord[0])
                    y.append(coord[1])
                    z.append(coord[2])
                    found=True
                    break
            if not found:
                x.append(np.nan)
                y.append(np.nan)
                z.append(np.nan)
    coords = pd.DataFrame({'x':x,'y':y,'z':z}).reset_index(drop=True)
    return coords