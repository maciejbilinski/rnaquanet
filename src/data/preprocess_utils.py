import glob
import os
import shutil
import subprocess
import torch
import h5py
import numpy as np
import multiprocessing as mp
import pandas as pd
import re
from tqdm import tqdm
from multiprocessing import Pool
from Bio.PDB import PDBParser
# from rnapolis import parser, annotator, tertiary
from pathlib import Path
from torch_geometric.data import Data
from typing import Literal

from config.config import ConfigData, RnaquanetConfig
from config.custom_types import PathType

def filter_file(pdb_filepaths: list[PathType], config: RnaquanetConfig) -> None:
    """
    Reads and filters specified PDB file.

    Args:
    - pdb_filepaths - list of PDB file paths relative to 'data/ares/archive'
    subdirectory
    - config - rnaquanet YML config file

    Returns:
    - None

    Raises exception if any of the files in 'pdb_filepaths' does not exist.
    """
    path = os.path.join('data', config.data.download.name)
    archive_path = os.path.join(path, 'archive')
    filtered_path = os.path.join(path, 'preprocessing', 'filtered')
    os.makedirs(filtered_path, exist_ok=True)

    print('Filtering PDB files...') 
    # For each input file   
    for filename in tqdm(pdb_filepaths, unit='f'):
        in_file_path = os.path.join(archive_path, filename)

        if not os.path.exists(in_file_path):
            raise Exception(f'Cannot filter file {in_file_path}: file does not exist. Perhaps you tried filtering before downloading?')
        
        out_file_path = os.path.join(filtered_path, filename)
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

        with open(in_file_path, 'r') as in_file:
            with open(out_file_path, 'w') as out_file:
                for line in in_file:
                    if line.startswith('ATOM') or line.startswith('TER'):
                        out_file.write(line)
            


def _rnagrowth_subprocess_func(params: tuple[RnaquanetConfig, PathType, PathType]):
    """
    Launches RNAgrowth tool and extracts features from PDB file.
    """
    config, in_filename, child = params
    s = subprocess.Popen(['java', '-jar', 'RNAgrowth.jar', os.path.basename(in_filename), config.features.atom_for_distance_calculations, config.features.max_euclidean_distance], stdout=subprocess.PIPE, cwd=child)
    s.wait()


def extract_features(pdb_filepaths: list[PathType], config: RnaquanetConfig) -> None:
    """
    Extracts features from specified PDB files.

    Args:
    - pdb_filepaths - list of PDB file paths relative to
    'data/ares/preprocessing/filtered' subdirectory
    - config - rnaquanet YML config file

    Returns:
    - None

    Exceptions:
    - if 'preprocessing/filtered' directory does not exist
    - if any of the files in 'pdb_filepaths' does not exist
    - if tools/RNAgrowth does not exist
    """
    # idk what it is used for - why import when disabling it in the next line?
    # import logging
    # logging.disable()
    config: ConfigData = config.data

    tool_path = os.path.join('tools', 'RNAgrowth')

    if not os.path.exists(tool_path):
        raise Exception("RNAgrowth tools ('tools/RNAgrowth') does not exist.")

    path = os.path.join('data', config.download.name, 'preprocessing')
    filtered_path = os.path.join(path, 'filtered')
    
    if not os.path.exists(filtered_path):
        raise Exception("Directory with filtered files ('preprocessing/filtered') not found. Perhaps you tried extracting features before filtering?")
    
    features_path = os.path.join(path, 'features')
    os.makedirs(features_path, exist_ok=True)

    # For each input file
    for filename in pdb_filepaths:
        in_file_path = os.path.join(filtered_path, filename)
        
        if not os.path.exists(in_file_path):
            raise Exception(f'Cannot extract features from file {in_file_path}: file does not exist. Perhaps you tried extracting features before filtering said file?')
        
        out_file_path = os.path.join(features_path, filename)
        # Copy file and its directories to the destination path
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
        shutil.copy(in_file_path, out_file_path)

    # RNAGrowth
    # For each subdirectory (e.g. 'train', 'test', ...)
    for subdir in os.listdir(features_path):
        subdir_path = os.path.join(features_path, subdir)
        if not os.path.isdir(subdir_path):
            continue
        
        subdir_path = os.path.join(features_path, subdir)
        rnagrowth_input_paths = glob.glob(f'{subdir_path}/*.pdb', recursive=True)

        # Copy RNAGrowth into subdirectory for efficient piping
        shutil.copytree(tool_path, subdir_path, dirs_exist_ok=True)
        
        print('Extracting features from PDB files...')
        
        with Pool(mp.cpu_count()) as pool:
            for _ in tqdm(enumerate(pool.imap_unordered(_rnagrowth_subprocess_func, [[config, in_filepath, subdir_path] for in_filepath in rnagrowth_input_paths])),
                          total=len(rnagrowth_input_paths), unit='f'):
                continue

        allowed_extensions = ['.bon', '.ang', '.atr', '.3dn']
        subdir_files = os.listdir(subdir_path)
        
        print(f'Cleaning subdirectory {subdir} from temporary files...')
        
        for filename in tqdm(subdir_files, unit='f'):
            file_path = os.path.join(subdir_path, filename)
            
            # Remove all files except for ['.bon', '.ang', '.atr', '.3dn']
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                os.remove(file_path)
    
    # Structure CSV
    for subdir in os.listdir(filtered_path):
        subdir_path = os.path.join(filtered_path, subdir)

        column_to_save = [config.download.rmsd_column_name, config.download.csv_structure_column_name]      
        df = pd.read_csv(os.path.join('data', config.download.name, 'archive', 'target.csv'), sep=config.download.rmsd_csv_delimiter)

        # Set of all *.pdb filenames without extensions
        file_names_without_ext = set([os.path.splitext(os.path.basename(file_path))[0] for file_path in glob.glob(f'{subdir_path}/*.pdb')])
 
        df.drop(list(set(df.columns.values.tolist()) - set(column_to_save)), axis=1, inplace=True)
        df['description'] = df['description'].str.replace('.pdb', '', regex=False)
        df.drop(df[~df['description'].isin(file_names_without_ext)].index, inplace=True)
        df.rename(columns={
            config.download.rmsd_column_name: 'target', 
            config.download.csv_structure_column_name: 'description'
        }, inplace=True)

        pdb_parser = PDBParser(QUIET=True)
        sequences = []
        pairings = ['.(((..((((((.)))).))...)))..'] # TODO temporary 4 testing

        print('Generating CSV...')
        for _, row in tqdm(df.iterrows(), total=len(df.index)):
            structure_pdb_path = os.path.join(os.path.abspath(Path()), filtered_path, subdir, f"{row['description']}.pdb")
            structure_pdb = pdb_parser.get_structure('structure', structure_pdb_path)

            for model in structure_pdb:
                temp_seq = []
                for chain in model:
                    temp_seq.append(''.join([re.sub(r'[^ATGCU]', '', residue.resname) for residue in chain]))
                sequences.append(''.join(temp_seq))
            
            # RNAPolis
            # with open(structure_pdb_path, 'r') as f:
            #     structure3d = parser.read_3d_structure(f)
            #     structure2d = annotator.extract_secondary_structure(structure3d)
            #     mapping = tertiary.Mapping2D3D(structure3d, structure2d, False)
            #     temp = []
            #     for index, row in enumerate(mapping.dot_bracket.split('\n')):
            #         if (index % 3) == 2:
            #             temp.append(row)
            #     pairings.append(''.join(temp))

        df['base_pairing'] = pairings
        df['sequence'] = sequences
        df = df.reset_index()
        df.drop('index', axis=1, inplace=True)
        df.to_csv(os.path.join(features_path, f'{subdir}.csv'))


def get_data_list(config: RnaquanetConfig) -> dict[list[Data]]:
    """
    Args:
    - config - rnaquanet YML config file

    Returns:
    - a dictionary containing lists of Data
    """
    config: ConfigData = config.data

    def get_node_features_from_csv(row: pd.Series, distinguish: bool = False) -> pd.DataFrame:
        """
        Gets node features from csv file.

        Args:
        - row - Pandas row of data
        - distinguish - True if distinguish between opening and closing
        parentheses during one hot encoding

        Returns:
        - Pandas dataframe with node features from csv
        """
        sequence = row['sequence']
        base_pairing = row['base_pairing']

        df = pd.DataFrame({
            'nucleotide': list(sequence),
            'dot_bracket': list(base_pairing)
        })
        series = pd.Categorical(
            df['dot_bracket'] if distinguish
            else df['dot_bracket'].replace({
                '\(': '()', '\)': '()', '\{': '{}', '\}': '{}', '\<': '<>', '\>': '<>', '\[': '[]', '\]': '[]'
            }, regex=True),
            categories=['.', '{', '}', '[', ']', '(', ')', '<', '>'] if distinguish else ['.', '{}', '()', '[]', '<>'])

        df = pd.concat([
            df,
            pd.get_dummies(pd.Categorical(df['nucleotide'], categories=['A', 'U', 'C', 'G']), prefix='nucleotide').astype(int),
            pd.get_dummies(series, prefix='dot_bracket').astype(int)
        ], axis=1)
        return df

    def get_node_features_from_file(path: str, row: pd.Series, file_type: Literal['bon', 'ang', 'atr'],
                                    nan_replacement: float = 0.0,
                                    exclude_columns: list[str] = ['Chain', 'ResNum', 'iCode', 'Name']
                                    ) -> pd.DataFrame:
        """
        Get features from a given file type.

        Args:
        - path - directory containing the files
        - row - Pandas row of data
        - file_type - type of file with sample's features (supported: bon, ang, atr)
        - nan_replacement - value representing a replacement for NaN values found
        - exclude_columns - list of columns which should be excluded

        Returns:
        - Pandas dataframe with features from chosen sample and file type
        """
        df: pd.DataFrame = pd.read_csv(
            os.path.join(path, f"{row['description']}.{file_type}"), sep='\t'
        )
        return (df.reset_index(drop=True)
                  .drop(columns=exclude_columns)
                  .replace('-', nan_replacement)
                  .fillna(nan_replacement)
                  .add_prefix(f'{file_type}_'))

    def get_edges(path: PathType, row: pd.Series) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Gets edges from a given csv file.

        Args:
        - path - path to csv file
        - row - Pandas row of data

        Returns:
        - a tuple of two torch Tensors
        """
        df = pd.read_csv(os.path.join(path,
                         f"{row['description']}_{config.features.max_euclidean_distance}.3dn"), sep='\t').reset_index(drop=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        dist = df.to_numpy(dtype=np.float32)
        pairs = np.vstack(np.where(dist > 0))
        edge_index = np.array([pairs[0, :], pairs[1, :]])
        edge_attr = np.array([[dist[start, end], (end - start + 1)] for start, end in pairs.T]) # end - start + 1 is sequentional distance
        return (torch.tensor(edge_index, dtype=torch.long), torch.tensor(edge_attr, dtype=torch.float32))

    path = os.path.join('data', config.download.name, 'preprocessing')
    features = os.path.join(path, 'features')
    data_lists = {}
    for child in os.listdir(features): # train / test
        name = child
        child = os.path.join(features, child)
        if os.path.isdir(child):
            df = pd.read_csv(os.path.join(features, f'{name}.csv'))
            print('Getting node features from csv...')
            progress_bar = tqdm(total=df.shape[0]+1, unit='f')
            data_lists[name] = []
            for i in range(df.shape[0]):
                try:
                    csv_features = get_node_features_from_csv(df.iloc[i]).add_prefix('csv_')
                    bon_features = get_node_features_from_file(child, df.iloc[i], 'bon')
                    ang_features = get_node_features_from_file(child, df.iloc[i], 'ang')
                    atr_features = get_node_features_from_file(child, df.iloc[i], 'atr')
                    x_df = pd.concat([
                        csv_features,
                        bon_features,
                        ang_features,
                        atr_features,
                    ], axis=1)
                    x = torch.from_numpy(
                        x_df.drop(columns=[
                            'csv_nucleotide', 'csv_dot_bracket',
                        ]).to_numpy(dtype=np.float32)
                    )
                    edge_index, edge_attr = get_edges(child, df.iloc[i])
                    y = torch.tensor(df.loc[i, 'target'], dtype=torch.float32)
                    data_lists[name].append(Data(x, edge_index, edge_attr, y))
                except FileNotFoundError as e:
                    print(f'{e.filename} was not found')
                progress_bar.update()
            progress_bar.update()
            progress_bar.close()

    return data_lists


def save_data_to_hdf5(config: RnaquanetConfig, filename: str, data_list: list[Data]):
    """
    Save a list of Data objects to an HDF5 file.

    Args:
    - config - rnaquanet YML config file
    - filename - name of the HDF5 file to be saved
    - data_list - list of Data objects to be saved
    """
    config: ConfigData = config.data

    with h5py.File(os.path.join('data', config.download.name, f'{filename}.h5'), 'w') as file:
        for i, data in enumerate(data_list):
            group = file.create_group(str(i))
            for key, value in data:
                if isinstance(value, torch.Tensor):
                    group.create_dataset(key, data=value.numpy())
                else:
                    group.attrs[key] = value


def load_data_from_hdf5(config: RnaquanetConfig, filename: str) -> list[Data]:
    """
    Load a list of Data objects from an HDF5 file.

    Args:
    - config - rnaquanet YML config file
    - filename - name of the HDF5 file to be loaded

    Returns:
    - data_list - list of Data objects loaded from the HDF5 file
    """
    data_list = []

    with h5py.File(os.path.join('data', config.data.download.name, f'{filename}.h5'), 'r') as file:
        for key in file.keys():
            data_dict = {f_key: torch.tensor(f_value[()])
                         if isinstance(f_value, h5py.Dataset)
                         else f_value
                         for f_key, f_value in file[key].items()}
            data = Data.from_dict(data_dict)
            data_list.append(data)

    return data_list
