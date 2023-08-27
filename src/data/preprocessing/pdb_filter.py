import os

from tqdm import tqdm
from src.config.custom_types import PathType
from rnaquanet import get_base_dir

def filter_file(file_path: PathType) -> str:
    """
    Reads and filters specified PDB file.

    Args:
    - file_path - PDB file absolute path  
    - config - rnaquanet YML config file

    Returns:
    - None

    Raises exception if the file in 'filename' does not exist.
    """
    data_path = os.path.join(get_base_dir(), 'data')
    filtered_path = os.path.join(data_path, 'preprocessing', 'filtered')
    os.makedirs(filtered_path, exist_ok=True)

    print('Filtering PDB files...') 

    if not os.path.exists(file_path):
        raise Exception(f'Cannot filter file from {file_path}: file does not exist. Perhaps you tried filtering before downloading?')
    
    out_file_path = os.path.join(filtered_path, os.path.splitext(os.path.basename(file_path))[0], os.path.basename(file_path))
    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

    with open(file_path, 'r') as in_file:
        with open(out_file_path, 'w') as out_file:
            for line in in_file:
                if line.startswith('ATOM') or line.startswith('TER'):
                    out_file.write(line)
    return out_file_path


def filter_files(pdb_filepaths: list[PathType]) -> None:
    """
    Reads and filters specified PDB file.

    Args:
    - pdb_filepaths - list of PDB file paths absolute
    - config - rnaquanet YML config file

    Returns:
    - None

    Raises exception if any of the files in 'pdb_filepaths' does not exist.
    """


    print('Filtering PDB files...') 
    # For each input file   
    for filename in tqdm(pdb_filepaths, unit='f'):
        filter_file(filename)

