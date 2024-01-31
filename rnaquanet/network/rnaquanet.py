import os
import torch
import pytorch_lightning as pl
from time import time_ns
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from rnaquanet.data.preprocessing.preprocess_utils import process_single_structure
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from pytorch_lightning.loggers import TensorBoardLogger
import pytorch_lightning as pl
from torch.optim import Adam
from torch.nn import (
    BatchNorm1d,
    Identity,
    ReLU,
    LeakyReLU,
    Linear,
    MSELoss
)
import torch.nn.functional as F
from torch_geometric.nn import (
    GATConv,
    GCNConv,
    Sequential,
    global_mean_pool,
    BatchNorm,
    TransformerConv
)
from torch_geometric.nn.models import (
    GAT
)
from torch_geometric.loader import DataLoader
import numpy as np
from rnaquanet.data.preprocessing.hdf5_utils import load_data_from_hdf5
from IPython.display import clear_output
from tqdm import tqdm
import matplotlib.pyplot as plt
from rnaquanet.network.h5_graph_dataset import H5GraphDataset
import math
import pandas as pd

def get_empty_model(key: str) -> Sequential:
    conv = None
    first_dropout = None
    if key == 'ares' or key == 'seg1':
        conv = GATConv
        first_dropout = 0.5
    elif key == 'seg2' or key == 'transfer_seg2_ares':
        conv = TransformerConv
        first_dropout = 0.5
    elif key == 'seg3':
        conv = TransformerConv
        first_dropout = 0.8
    else:
        raise 'Unknown model key'


    return Sequential('x, edge_index, edge_attr, batch', [
        (conv(in_channels=99, out_channels=256, heads=4, dropout=first_dropout), f'x, edge_index{", edge_attr" if conv == GATConv else ""} -> x'),
        (BatchNorm(in_channels=256*4), 'x -> x'),
        (ReLU(), 'x -> x'),
        
        (conv(in_channels=256*4, out_channels=256, heads=8, dropout=0.5), f'x, edge_index{", edge_attr" if conv == GATConv else ""} -> x'),
        (BatchNorm(in_channels=256*8), 'x -> x'),
        (ReLU(), 'x -> x'),

        (GCNConv(in_channels=256*8, out_channels=256), 'x, edge_index -> x'),
        (global_mean_pool, 'x, batch -> x'),

        (Linear(in_features=256, out_features=64), 'x -> x'),
        (ReLU(), 'x -> x'),
        (Linear(in_features=64, out_features=1), 'x -> x'),
    ])

def get_model(key: str) -> Sequential:
    model = get_empty_model(key)
    model.load_state_dict(torch.load(f'/app/models/{key}.pt'))

    if key == 'transfer_seg2_ares':
        # freeze all layers except MLP
        for child in model.children():
            if type(child) != Linear:
                for param in child.parameters():
                    param.requires_grad = False
                    
    return model

def get_rmsd(model_name: str, path_to_pdb: str, config_path: str = '/app/config.yml', nan_replacement: float = 1000) -> float:
    model = get_model(model_name)
    model.eval()

    config = RnaquanetConfig(config_path)

    _, data = process_single_structure([path_to_pdb, config, None])
    for sample in DataLoader([data], batch_size=1):
        return model(torch.nan_to_num(sample.x, nan=nan_replacement), sample.edge_index, sample.edge_attr, sample.batch).item()