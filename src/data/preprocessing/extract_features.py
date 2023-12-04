import os
import shutil
import subprocess
from shutil import copyfile
from src.config.config import ConfigData, RnaquanetConfig
from rnaquanet import get_base_dir


def _rnagrowth_subprocess_func(config:ConfigData, in_filename:str, child:str):
    """
    Launches RNAgrowth tool and extracts features from PDB file.
    """

    copyfile(os.path.join(get_base_dir(),'tools','RNAgrowth','completeAtomNames.dict'), os.path.join(child, 'completeAtomNames.dict'))
    copyfile(os.path.join(get_base_dir(),'tools','RNAgrowth','config.properties'), os.path.join(child, 'config.properties'))
    copyfile(in_filename, os.path.join(child,os.path.basename(in_filename)))

    s = subprocess.Popen(['java', '-jar', os.path.join(get_base_dir(),'tools','RNAgrowth','RNAgrowth.jar'), os.path.join(child,os.path.basename(in_filename)), config.features.atom_for_distance_calculations, config.features.max_euclidean_distance], stdout=subprocess.PIPE, cwd=child)
    s.wait()

    os.remove(os.path.join(child,'completeAtomNames.dict')) 
    os.remove(os.path.join(child,'config.properties')) 
    os.remove(os.path.join(child,os.path.basename(in_filename))) 
    os.remove(os.path.join(child,'rnagrowth.log'))

def extract_features_files(filtered_file_path: str, config: ConfigData) -> None:
    """
    Extracts features from specified PDB files.

    Args:
    - filtered_file_path - PDB file absolute path 
    - config - rnaquanet YML config file

    Returns:
    - None

    Exceptions:
    - if 'preprocessing/filtered' directory does not exist
    - if any of the files in 'pdb_filepaths' does not exist
    - if tools/RNAgrowth does not exist
    """


    tool_path = os.path.join('tools', 'RNAgrowth')

    if not os.path.exists(tool_path):
        raise Exception("RNAgrowth tools ('tools/RNAgrowth') does not exist.")

    preprocessing_path = os.path.join(get_base_dir(), 'data', 'preprocessing')

    features_path = os.path.join(preprocessing_path, 'features')

    os.makedirs(features_path, exist_ok=True)
    features_file_path = os.path.join(features_path, os.path.splitext(os.path.basename(filtered_file_path))[0]) # feature/1ffk_/*.*
    
    if not os.path.exists(filtered_file_path):
        raise Exception(f"Filtered file {filtered_file_path} not found. Perhaps you tried extracting features before filtering?")
    

    if os.path.exists(features_file_path):
        if not config.features.regenerate_features_when_exists:
            return
        else:
            shutil.rmtree(features_file_path)

    os.makedirs(features_file_path, exist_ok=True)
    
    _rnagrowth_subprocess_func(config, filtered_file_path, features_file_path)





           