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
from rnapolis import parser, annotator, tertiary
from pathlib import Path
from torch_geometric.data import Data
from typing import Literal

from config.config import ConfigData, RnaquanetConfig
from config.types import PathType

def filter_files(config: RnaquanetConfig):
    """
    Reads and filters each PDB file in the 'train' and 'test' subfolders.

    Args:
    - config - rnaquanet YML config file
    """
    # Find all PDB files within directory and subdirectories
    config = config.data.download
    path = os.path.join('data', config.name)
    if os.path.exists(path):
        src = os.path.join(path, 'archive')
        if os.path.exists(src):
            dest = os.path.join(path, 'preprocessing', 'filtered')
            os.makedirs(dest)
            pattern = f'{src}/**/*.pdb'
            src_files = glob.glob(pattern, recursive=True)

            # Progress bar
            total_files = len(src_files)+1
            print('Filtering PDB files...')
            progress_bar = tqdm(total=total_files, unit='f')

            for in_filename in src_files:
                out_filename = in_filename.replace(src, dest)
                out_dir = os.path.dirname(out_filename)
                
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)

                with open(in_filename, 'r') as input_file:
                    with open(out_filename, 'w') as output_file:
                        for line in input_file:
                            if line.startswith('ATOM') or line.startswith('TER'):
                                output_file.write(line)
                
                progress_bar.update()
            
            progress_bar.update()
            progress_bar.close()
            return
        
    raise Exception(f'Cannot preprocess dataset before downloading')


def _loop_func(params: tuple[RnaquanetConfig, PathType, PathType]):
    config, in_filename, child = params
    s = subprocess.Popen(['java', '-jar', 'RNAgrowth.jar', os.path.basename(in_filename), config.features.atom_for_distance_calculations, config.features.max_euclidean_distance], stdout=subprocess.PIPE, cwd=child)
    s.wait()


def extract_features(config: RnaquanetConfig):
    """
    Extracts features from PDB files.

    Args:
    - config - rnaquanet YML config file
    """
    import logging
    logging.disable()
    config: ConfigData = config.data

    tool_path = os.path.join('tools', 'RNAgrowth')

    if not os.path.exists(tool_path):
        raise Exception('RNAgrowth tools does not exist')

    path = os.path.join('data', config.download.name, 'preprocessing')
    src = os.path.join(path, 'filtered')
    dest = os.path.join(path, 'features')

    if os.path.exists(src) and not os.path.exists(dest):
        # RNAGrowth
        shutil.copytree(src, dest)

        for child in os.listdir(dest):
            child = os.path.join(dest, child)
            pattern = f'{child}/*.pdb'
            src_files = glob.glob(pattern, recursive=True)
            total_files = len(src_files) + 1
            print('Extracting features...')
            progress_bar = tqdm(total=total_files, unit='f')

            shutil.copytree(tool_path, child, dirs_exist_ok=True)
            with Pool(mp.cpu_count()) as pool:
                for _ in pool.imap_unordered(_loop_func, [[config, in_filename, child] for in_filename in src_files])[1:]:
                    progress_bar.update()

            progress_bar.update()
            progress_bar.close()

            allowed_extensions = [".bon", ".ang", ".atr", ".3dn"]
            files = os.listdir(child)
            total_files = len(files) + 1
            progress_bar = tqdm(total=total_files, unit='f')
            for filename in files:
                file_path = os.path.join(child, filename)
                if not any(filename.endswith(ext) for ext in allowed_extensions):
                    os.remove(file_path)
                progress_bar.update()
            progress_bar.update()
            progress_bar.close()

        # structure CSV
        for child in os.listdir(src):
            folder_name = child
            child = os.path.join(src, child)

            column_to_save = [config.download.rmsd_column_name, config.download.csv_structure_column_name]      
            df = pd.read_csv(os.path.join('data', config.download.name, 'archive', 'target.csv'), sep=config.download.rmsd_csv_delimiter)
            extracted_structures = set([filename.split('/')[-1].split('.')[0] for filename in glob.glob(f'{child}/*.pdb')])
            df.drop(list(set(df.columns.values.tolist()) - set(column_to_save)), axis=1, inplace=True)
            df['description'] = df['description'].str.replace('.pdb', '', regex=False)
            df.drop(df[~df['description'].isin(extracted_structures)].index, inplace=True)
            df.rename(columns={
                config.download.rmsd_column_name: 'target', 
                config.download.csv_structure_column_name: 'description'
            }, inplace=True)

            pdb_parser = PDBParser(QUIET=True)
            sequences = []
            pairings = []

            progress_bar = tqdm(total=len(df.index))
            for index, row in df.iterrows():
                structure_pdb_path = os.path.join(str(Path().absolute()), src, folder_name, f"{row['description']}.pdb")
                structure_pdb = pdb_parser.get_structure("structure", structure_pdb_path)

                for model in structure_pdb:
                    temp_seq = []
                    for chain in model:
                        temp_seq.append(''.join([re.sub(r'[^ATGCU]', '', residue.resname) for residue in chain]))
                    sequences.append(''.join(temp_seq))
                
                with open(structure_pdb_path, 'r') as f:
                    structure3d = parser.read_3d_structure(f)
                    structure2d = annotator.extract_secondary_structure(structure3d)
                    mapping = tertiary.Mapping2D3D(structure3d, structure2d, False)
                    temp = []
                    for index, row in enumerate(mapping.dot_bracket.split('\n')):
                        if (index % 3) == 2:
                            temp.append(row)
                    pairings.append(''.join(temp))

                progress_bar.update(1)
            progress_bar.close()
            df['base_pairing'] = pairings
            df['sequence'] = sequences
            df = df.reset_index()
            df.drop('index', axis=1, inplace=True)
            df.to_csv(os.path.join(dest, f'{folder_name}.csv'))
        return

    raise Exception(f'Cannot preprocess dataset before downloading or filtering')


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
