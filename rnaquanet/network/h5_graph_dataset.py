import torch
import h5py
from torch.utils.data import Dataset
from torch_geometric.data import Data

class H5GraphDataset(Dataset):
    def __init__(self, filename):
        self.filename = filename
        self.collection = None

    def __getitem__(self, idx) -> Data:
        if self.collection is None:
            raise ValueError('To get length of dataset you have to first call __enter__ method or use "with" statement')
        value = self.collection[self.keys[idx]]
        if isinstance(value, h5py.Group):
            return Data(
                x=torch.tensor(value['x'][()]),
                edge_index=torch.tensor(value['edge_index'][()]),
                edge_attr=torch.tensor(value['edge_attr'][()]),
                y=torch.tensor(value['y'][()]) if value.get('y') is not None else None
            )
        else:
            raise ValueError('Given H5 file does not contain only H5 Groups')


    def __len__(self) -> int:
        if self.collection is None:
            raise ValueError('To get length of dataset you have to first call __enter__ method or use "with" statement')
        return len(self.collection.values())
    
    def __enter__(self):
        self.collection = h5py.File(self.filename, 'r')
        self.collection.__enter__()
        self.keys = list(self.collection.keys())
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.collection.__exit__()
        self.collection = None