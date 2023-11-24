import torch
import h5py

from torch_geometric.data import Data



def save_data_to_hdf5(file_path: str, data_list: list[Data]) -> None:
    """
    Save a list of Data objects to an HDF5 file.

    Args:
    - config - rnaquanet YML config file
    - filename - name of the HDF5 file to be saved
    - data_list - list of Data objects to be saved

    Returns:
    - None
    """

    with h5py.File(file_path, 'w') as file:
        for i, data in enumerate(data_list):
            group = file.create_group(str(i))
            for key, value in data:
                if isinstance(value, torch.Tensor):
                    group.create_dataset(key, data=value.numpy())
                else:
                    group.attrs[key] = value

def concat_hdf5_files(file_path: str, files_to_concat_path: list[str]) -> None:
    """
    Save a list of Data objects to an HDF5 file.

    Args:
    - file_path - .h5 output file
    - files_to_concat_path - [regex] files path to concat

    Returns:
    - None
    """

    with h5py.File(file_path, 'w') as file:
        for i, file_path in enumerate(files_to_concat_path):
            group = file.create_group(str(i))
            for element in load_data_from_hdf5(file_path):
                for key, value in element:
                    if isinstance(value, torch.Tensor):
                        group.create_dataset(key, data=value.numpy())
                    else:
                        group.attrs[key] = value

def load_data_from_hdf5(file_path: str) -> list[Data]:
    """
    Load a list of Data objects from an HDF5 file.

    Args:
    - config - rnaquanet YML config file
    - filename - name of the HDF5 file to be loaded relative to 'data/ares'
    directory

    Returns:
    - list of Data objects loaded from the HDF5 file
    """
    data_list = []

    with h5py.File(file_path, 'r') as file:
        for key in file.keys():
            data_dict = {f_key: torch.tensor(f_value[()])
                         if isinstance(f_value, h5py.Dataset)
                         else f_value
                         for f_key, f_value in file[key].items()}
            data = Data.from_dict(data_dict)
            data_list.append(data)

    return data_list

