import os
import torch
import numpy as np
import pandas as pd


from rnaquanet.utils.custom_types import PathType
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig



def get_edges(config: RnaquanetConfig, path: PathType) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Gets edges from a given csv file.

    Args:
    - path - absolute path to structure feature directory
    - row - Pandas row of data

    Returns:
    - a tuple of two torch Tensors
    """
    file_name_3dn = f"{os.path.splitext(os.path.basename(path))[0]}_{config.data.features.max_euclidean_distance}.3dn"
    df = pd.read_csv(os.path.join(path, file_name_3dn), sep='\t').reset_index(drop=True)

    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    dist = df.to_numpy(dtype=np.float32)
    pairs = np.vstack(np.where(dist > 0))
    edge_index = np.array([pairs[0, :], pairs[1, :]])
    edge_attr = np.array([[dist[start, end], (end - start + 1)] for start, end in pairs.T]) # end - start + 1 is sequentional distance
    return (torch.tensor(edge_index, dtype=torch.long), torch.tensor(edge_attr, dtype=torch.float32))