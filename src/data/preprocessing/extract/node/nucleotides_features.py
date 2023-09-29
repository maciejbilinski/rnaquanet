import pandas as pd
import re

from Bio.PDB import PDBParser


from src.config.custom_types import PathType

def extract_nucleotides(filtered_pdb_file_path: PathType) -> pd.DataFrame:
    pdb_parser = PDBParser(QUIET=True)
    sequences = []

    structure_pdb = pdb_parser.get_structure('structure', filtered_pdb_file_path)
    for model in structure_pdb:
        for chain in model:
            for residue in chain:
                sequences.append(re.sub(r'[^ATGCU]', '', residue.resname))
    df = pd.DataFrame({ 'nucleotide': sequences})
        
    return pd.get_dummies(pd.Categorical(df['nucleotide'], categories=['A', 'U', 'C', 'G']), prefix='nucleotide').astype(int)