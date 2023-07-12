import torch
from torch.utils.data import Dataset
from torch import Tensor
from typing import Any
import pandas as pd
from os import path
import numpy as np

class RNADataset(Dataset):
    def __init__(self, features_dir_path: str, csv_file_path: str, spacial_threshold: str = '16.0'):
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
            pd.get_dummies(df['nucleotide'], prefix='nucleotide'),
            pd.get_dummies(series, prefix='dot_bracket')
        ], axis=1)
        return df
    
    def get_node_features_from_bon(self, index):
        df = pd.read_csv(path.join(self.features_dir_path, self.samples.loc[index, 'description'] + '.bon'), sep='\t')
        replacement = 0 # TODO: verify that 0 is good replacement
        return df.reset_index(drop=True).drop(columns=[
            'Chain', 'ResNum', 'iCode', 'Name'
        ]).replace('-', replacement).fillna(replacement)
    
    def get_edges(self, index):
        df = pd.read_csv(path.join(self.features_dir_path, self.samples.loc[index, 'description'] + '_' + self.spacial_threshold + '.3dn'), sep='\t').reset_index(drop=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        dist = df.to_numpy(dtype=np.float32)
        pairs = np.vstack(np.where(dist > 0))
        edge_index = np.array([pairs[0, :], pairs[1, :]])
        edge_attr = np.array([[dist[start, end]] for start, end in pairs.T])
        return torch.tensor(edge_index, dtype=torch.long), torch.tensor(edge_attr, dtype=torch.float32)
    
    def __getitem__(self, index):
        csv_features = self.get_node_features_from_csv(index).add_prefix('csv_')
        bon_features = self.get_node_features_from_bon(index).add_prefix('bon_')
        x_df = pd.concat([
            csv_features,
            bon_features
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
        return x_df, x, edge_index, edge_attr, y #TODO: remove x_df
    
if __name__ == '__main__':
    dataset = RNADataset('', 'train_df.csv')
    test = dataset.__getitem__(0)
    print(test[1])
    print()
    print(test[0].head())
