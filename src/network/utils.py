import numpy as np
from typing import Tuple
from torch_geometric.data import Batch
import torch

def round_to_pow2(value):
    return np.exp2(np.round(np.log2(value))).astype(int)

def layer_sizes_linear(in_feats, out_feats, layers, round_pow2=False):
    sizes = np.linspace(in_feats, out_feats, layers + 1).round().astype(np.int32)
    if round_pow2:
        sizes[1:-1] = round_to_pow2(sizes[1:-1])
    return sizes.tolist()

def layer_sizes_exp2(in_feats, out_feats, layers, round_pow2=False) -> list[int]:
    sizes = (
        np.logspace(np.log2(in_feats), np.log2(out_feats), layers + 1, base=2)
        .round()
        .astype(np.int32)
    )
    if round_pow2:
        sizes[1:-1] = round_to_pow2(sizes[1:-1])
    return sizes.tolist()
    
def extract_batch(graphs: Batch) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    x = graphs.x
    edge_index = graphs.edge_index
    edge_attr = graphs.edge_attr
    batch = graphs.batch
    y = graphs.y

    return x, edge_index, edge_attr, batch, y