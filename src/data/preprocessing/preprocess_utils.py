import os
import torch
import numpy as np
import pandas as pd

from rnaquanet import get_base_dir
from torch_geometric.data import Data

from src.config.config import ConfigData, RnaquanetConfig
from src.data.preprocessing.extract.edge.edge_features import get_edges
from src.data.preprocessing.extract.node.basepairs_features import extract_basepairs
from src.data.preprocessing.extract.node.files_features import get_features_from_file
from src.data.preprocessing.extract.node.nucleotides_features import extract_nucleotides
from src.data.preprocessing.extract_features import extract_features_files
from src.data.preprocessing.hdf5_utils import save_data_to_hdf5
from src.data.preprocessing.pdb_filter import filter_file

def process_structure_f(params: tuple[str, ConfigData, str, float]):
    """
    Launches process_structure.
    """
    file_path, config, output_h5_dir, target = params
    process_structure(file_path, config, output_h5_dir, target)

def process_structure(file_path:str, config: RnaquanetConfig, output_h5_dir:str, target:float=None):
    """
    Full structure processing pipeline

    Args:
    - file_path - PDB file path absolute
    - config - rnaquanet YML config file
    - output_h5_dir - directory name to store .h5 results
    - target - optional parameter for y value

    Returns:
    - torch_geometric.data.Data result

    Raises exception if any of the files in 'features_file_path' does not exist.
    """
    config_c: ConfigData = config.data

    filtered_file_path = filter_file(file_path)

    structure_file_name = os.path.splitext(os.path.basename(filtered_file_path))[0]

    features_path = os.path.join(get_base_dir(), 'data', 'preprocessing', 'features')
    features_file_path = os.path.join(features_path, structure_file_name) 

    extract_features_files(filtered_file_path, config_c)
    sequence_feature = extract_nucleotides(filtered_file_path)
    basepairs_feature = extract_basepairs(filtered_file_path)

    try:
        bon_features = get_features_from_file(features_file_path, 'bon')
        ang_features = get_features_from_file(features_file_path, 'ang')
        atr_features = get_features_from_file(features_file_path, 'atr')
        x_df = pd.concat([
            sequence_feature,
            basepairs_feature,
            bon_features,
            ang_features,
            atr_features
        ], axis=1)
        x = torch.from_numpy(
            x_df.to_numpy(dtype=np.float32)
        )
        edge_index, edge_attr = get_edges(features_file_path, config_c)

        output=Data(x, edge_index, edge_attr, y=target)
        os.makedirs(output_h5_dir, exist_ok=True)
        
        save_data_to_hdf5(os.path.join(output_h5_dir, structure_file_name+'_target.h5' \
                                                if target is not None else structure_file_name+'.h5'), [output])
        return output

    except FileNotFoundError as e:
        print(f'File {e.filename} was not found. Perhaps you tried returning data list without prior feature extraction?')
        return
    