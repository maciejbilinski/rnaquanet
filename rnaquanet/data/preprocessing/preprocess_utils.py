import glob
import os
import torch
import numpy as np
import pandas as pd
from multiprocessing import Pool
import multiprocessing as mp

from torch_geometric.data import Data
from rnaquanet.data.preprocessing.hdf5_utils import concat_hdf5_files, save_data_to_hdf5

from rnaquanet.utils.dataclasses import ConfigData
from rnaquanet.utils.inputs import InputsConfig
from rnaquanet.utils.prepare_target_set import read_target_csv
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from rnaquanet.utils.safe_tqdm import SafeTqdm
from .extract.edge.edge_features import get_edges
from .extract.node.basepairs_features import extract_basepairs
from .extract.node.files_features import get_features_from_file
from .extract.node.nucleotides_features import extract_nucleotides
from .extract_features import extract_features
from .pdb_filter import filter_file

def process_single_structure(params: tuple[str, RnaquanetConfig, float|None]) -> tuple[str, Data]:
    """
    Process single structure

    Args:
    - file_path - absolute PDB file path
    - config - rnaquanet config
    - target - optional parameter for y value

    Returns:
    - structure_name, Data object which can be used in neural network

    Raises exception if any of the files in 'features_file_path' does not exist.
    """
    file_path, config, target = params
    structure_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # filtering
    filtered_file_path = filter_file(config, file_path)

    # extract features
    features_file_path = extract_features(config, filtered_file_path)
    sequence_feature = extract_nucleotides(filtered_file_path)
    basepairs_feature = extract_basepairs(filtered_file_path)

    # parse features
    try:
        bon_features = get_features_from_file(config, features_file_path, 'bon')
        ang_features = get_features_from_file(config, features_file_path, 'ang')
        atr_features = get_features_from_file(config, features_file_path, 'atr')
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
        if target is not None:
            target = torch.tensor(target)

        edge_index, edge_attr = get_edges(config, features_file_path)
        output = Data(x, edge_index, edge_attr, y=target)
        return structure_name, output
    except FileNotFoundError as e:
        e.add_note(f'File {e.filename} was not found. Perhaps you tried returning data list without prior feature extraction?')
        raise


    

def process_structures(config: RnaquanetConfig):
    """
    Full structure processing pipeline

    Args:
    - file_path - PDB file path absolute
    - config - rnaquanet YML config file
    - output_h5_dir - directory name to store .h5 results
    - target - optional parameter for y value

    Returns:
    - torch_geometric.data.Data result

    """
    ic = InputsConfig(config)
    for dataset in ['train', 'val', 'test']:
        df = read_target_csv(config, dataset)
        if dataset == 'train':
            files = ic.TRAIN_FILES
        elif dataset == 'val':
            files = ic.VAL_FILES
        else:
            files = ic.TEST_FILES

        with Pool(mp.cpu_count()) as pool:
            path = os.path.join(config.data.path, config.name, 'h5', dataset)
            os.makedirs(path, exist_ok=True)
            print(f'Preprocessing {dataset} dataset')
            for _, output in SafeTqdm(
                config,
                enumerate(
                    pool.imap_unordered(
                        process_single_structure,
                        [
                            [
                                structure,
                                config,
                                df[
                                    df["description"] == os.path.splitext(os.path.basename(structure))[0]
                                ]["target"].item(),
                            ]
                            for structure in files if len(df[
                                df["description"] == os.path.splitext(os.path.basename(structure))[0]
                            ]["target"]) == 1
                        ],
                    )
                ),
                total=len(files),
                unit="f",
            ):
                structure_name, data = output
                save_data_to_hdf5(
                    structure_name,
                    os.path.join(path, f'{structure_name}.h5'),
                    data
                )
        concat_hdf5_files(
            os.path.join(config.data.path, config.name, f'{dataset}.h5'),
            glob.glob(
                os.path.join(
                    path,
                    "*.h5",
                )
            ),
        )


    

    
    