import os

from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from rnaquanet.utils.custom_types import PathType

def filter_file(config: RnaquanetConfig, file_path: PathType) -> str:
    """
    Reads and filters specified PDB file.

    Args:
    - file_path - PDB file absolute path  
    - config - rnaquanet YML config file

    Returns:
    - path to filtered PDB file

    Raises exception if the file in 'filename' does not exist.
    """
    filtered_path = os.path.join(config.data.path, config.name, 'preprocessing', 'filtered')
    os.makedirs(filtered_path, exist_ok=True)


    if not os.path.exists(file_path):
        raise Exception(f'Cannot filter file from {file_path}: file does not exist. Perhaps you tried filtering before downloading?')
    
    out_file_path = os.path.join(filtered_path, os.path.basename(file_path))
    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

    with open(file_path, 'r') as in_file:
        with open(out_file_path, 'w') as out_file:
            for line in in_file:
                if line.startswith('ATOM') or line.startswith('TER'):
                    out_file.write(line)
    return out_file_path

