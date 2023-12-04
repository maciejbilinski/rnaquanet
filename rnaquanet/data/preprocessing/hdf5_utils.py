import torch
import h5py

from torch_geometric.data import Data



def save_data_to_hdf5(structure_name: str, file_path: str, data: Data) -> None:
    """
    Save a single Data object to an HDF5 file.

    Args:
    - structure_name - structure name
    - file_path - path to HDF5 file to be saved
    - data_list - list of Data objects to be saved

    Returns:
    - None
    """

    with h5py.File(file_path, 'w') as file:
        group = file.create_group(structure_name)
        group.create_dataset('x', data=data.x.numpy())
        group.create_dataset('edge_index', data=data.edge_index.numpy())
        group.create_dataset('edge_attr', data=data.edge_attr.numpy())
        if data.y is not None:
            group.create_dataset('y', data=data.y.numpy())

def concat_hdf5_files(file_path: str, files_to_concat_path: list[str]) -> None:
    """
    Save a list of Data objects to an HDF5 file.

    Args:
    - file_path - .h5 output file
    - files_to_concat_path - [regex] files path to concat

    Returns:
    - None
    """

    with h5py.File(file_path, 'w') as output:
        for file_path in files_to_concat_path:
            with h5py.File(file_path, 'r') as input:
                for key, value in input.items(): # key is structure name
                    if isinstance(value, h5py.Group):
                        input.copy(key, output)


def load_data_from_hdf5(file_path: str) -> list[Data]:
    """
    Load a list of Data objects from an HDF5 file.

    Returns:
    - list of Data objects loaded from the HDF5 file
    """
    data_list = []

    with h5py.File(file_path, 'r') as file:
        for key, value in file.items(): # key is structure name
            if isinstance(value, h5py.Group):
                data_list.append(Data(
                    x=torch.tensor(value['x'][()]),
                    edge_index=torch.tensor(value['edge_index'][()]),
                    edge_attr=torch.tensor(value['edge_attr'][()]),
                    y=torch.tensor(value['y'][()]) if value.get('y') is not None else None
                ))

    return data_list

