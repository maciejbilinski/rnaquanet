import torch
from torch.utils.data import Dataset
import pandas as pd
from os import path
import numpy as np
from tqdm import tqdm
from .CONFIG import to_csv as params
from .CONFIG import change_dir
import argparse


class RNADatasetPreparation:
    def __init__(self, features_dir_path: str, csv_file_path: str, spacial_threshold: str = str(params.max_euclidean_distance)):
        """
        args:
        - spacial_threshold: str - the value of the last parameter of the program used to generate information defining the edges and describing the vertices of the graph; the maximum permissible Euclidean distance between a pair of atoms in 3D space measured in Angstroms, which cannot be exceeded for us to consider those atoms to be located relatively close to each other in spatial proximity
        """
        self.features_dir_path = features_dir_path
        self.samples = pd.read_csv(path.join(features_dir_path, csv_file_path))
        self.spacial_threshold = spacial_threshold

    def __len__(self) -> int:
        return self.samples.shape[0]

    def get_node_features_from_csv(self, index, distinguish: bool = False):
        """
        args:
        - distinguish: bool - True if distinguish between opening and closing parentheses during one hot encoding
        """

        sequence = self.samples.loc[index, 'sequence']
        base_pairing = self.samples.loc[index, 'base_pairing']

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
            pd.get_dummies(df['nucleotide'], prefix='nucleotide').astype(int),
            pd.get_dummies(series, prefix='dot_bracket').astype(int)
        ], axis=1)
        return df

    def get_node_features_from_file(self, index: int, file_type: str,
                                    nan_replacement: float = 0.0,
                                    exclude_columns: list[str] = ['Chain', 'ResNum', 'iCode', 'Name']
                                    ) -> pd.DataFrame:
        """Get features from given file type.

        args:
        - index: int - sample index
        - file_type: str - type of file with sample's features (supported: bon, ang, atr) 
        - nan_replacement: float - value representing a replacement for NaN values found
        - exclude_columns: list[str] - list of columns which should be excluded

        return:
        - Dataframe with features from chosen sample and file type
        """

        df: pd.DataFrame = pd.read_csv(
            path.join(self.features_dir_path, f"{self.samples.loc[index, 'description']}_filtered.{file_type}"), sep='\t'
        )
        return (df.reset_index(drop=True)
                  .drop(columns=exclude_columns)
                  .replace('-', nan_replacement)
                  .fillna(nan_replacement)
                  .add_prefix(f'{file_type}_'))

    def get_edges(self, index):
        df = pd.read_csv(path.join(self.features_dir_path,
                         f"{self.samples.loc[index, 'description']}_filtered_{self.spacial_threshold + '.3dn'}"), sep='\t').reset_index(drop=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        dist = df.to_numpy(dtype=np.float32)
        pairs = np.vstack(np.where(dist > 0))
        edge_index = np.array([pairs[0, :], pairs[1, :]])
        edge_attr = np.array([[dist[start, end]] for start, end in pairs.T])
        return torch.tensor(edge_index, dtype=torch.long), torch.tensor(edge_attr, dtype=torch.float32)

    def __getitem__(self, index):
        # TODO: for each file - verify that 0 is good replacement
        # it can be added as `nan_replacement=` argument if needed
        csv_features = self.get_node_features_from_csv(index).add_prefix('csv_')
        bon_features = self.get_node_features_from_file(index, 'bon')
        ang_features = self.get_node_features_from_file(index, 'ang')
        atr_features = self.get_node_features_from_file(index, 'atr')
        x_df = pd.concat([
            csv_features,
            bon_features,
            ang_features,
            atr_features,
            # TODO: add more node features
        ], axis=1)
        x = torch.from_numpy(
            x_df.drop(columns=[
                'csv_nucleotide', 'csv_dot_bracket',
                # TODO: drop non-numeric columns
            ]).to_numpy(dtype=np.float32)
        )
        edge_index, edge_attr = self.get_edges(index)
        y = torch.tensor(self.samples.loc[index, 'new_rms'], dtype=torch.float32)
        return x_df, x, edge_index, edge_attr, y  # TODO: remove x_df
    
    def prepare_data(self, output_path: str, output_file: str):
        df = None
        df_edge = None
        # Progress bar
        total_files = self.__len__()+1
        progress_bar = tqdm(total=total_files, unit='f')

        for i in range(self.__len__()):
            x_df, _, edge_index, edge_attr, y = self.__getitem__(i)
            x_df['description'] = self.samples.loc[i, 'description']
            x_df['new_rms'] = y.item()
            df_edge_temp = pd.DataFrame(torch.cat((edge_index.T, edge_attr), axis=1).numpy(), columns=['begin_node', 'end_node', 'distance'])
            df_edge_temp['description'] = self.samples.loc[i, 'description']

            if df is None:
                df = x_df
                df_edge = df_edge_temp
            else:
                df = pd.concat([df, x_df], axis=1)
                df_edge = pd.concat([df_edge, df_edge_temp], axis=1)
            
            if i % 500 == 0:
                df.to_csv(path.join(output_path, f'{output_file}_nodes.csv'), index = False)
                df_edge.to_csv(path.join(output_path, f'{output_file}_edges.csv'), index = False)
            progress_bar.update()

        df.to_csv(path.join(output_path, f'{output_file}_nodes.csv'), index = False)
        df_edge.to_csv(path.join(output_path, f'{output_file}_edges.csv'), index = False)
        progress_bar.close()


if __name__ == '__main__':
    change_dir('..')
    # TODO: argparser

    # get output filename
    output_filename = path.splitext(params.csv_filename)[0]

    dataset = RNADatasetPreparation(params.features_dir_path, params.csv_filename)
    dataset.prepare_data(params.output_path, output_filename)
    