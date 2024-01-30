import torch
import h5py
from torch.utils.data import Dataset
from torch_geometric.data import Data
import random

class H5GraphDataset(Dataset):
    def __init__(self, filename, max_iterations = None, nan_replacement = 1000, return_key = False):
        self.filename = filename
        self.collection = None
        self.max_iterations = max_iterations
        self.nan = nan_replacement
        self.return_key = return_key

    def shuffle(self):
        random.shuffle(self.keys)

    def __getitem__(self, idx) -> Data:
        if self.collection is None:
            raise ValueError('To get length of dataset you have to first call __enter__ method or use "with" statement')
        value = self.collection[self.keys[idx]]
        if isinstance(value, h5py.Group):
            if self.return_key:
                return self.keys[idx], Data(
                    x=torch.nan_to_num(torch.tensor(value['x'][()]), nan=self.nan),
                    edge_index=torch.tensor(value['edge_index'][()]),
                    edge_attr=torch.tensor(value['edge_attr'][()]),
                    y=torch.tensor(value['y'][()]) if value.get('y') is not None else None
                )
            else:
                return Data(
                    x=torch.nan_to_num(torch.tensor(value['x'][()]), nan=self.nan),
                    edge_index=torch.tensor(value['edge_index'][()]),
                    edge_attr=torch.tensor(value['edge_attr'][()]),
                    y=torch.tensor(value['y'][()]) if value.get('y') is not None else None
                )
        else:
            raise ValueError('Given H5 file does not contain only H5 Groups')


    def __len__(self) -> int:
        if self.collection is None:
            raise ValueError('To get length of dataset you have to first call __enter__ method or use "with" statement')
        if self.max_iterations is None:
            return len(self.collection.values())
        else:
            return self.max_iterations

    def __enter__(self):
        self.collection = h5py.File(self.filename, 'r')
        self.collection.__enter__()
        self.keys = list(self.collection.keys())
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.collection.__exit__()
        self.collection = None
