import sys
import os
from omegaconf import OmegaConf
import torch
from torch_geometric.data import Data, Batch
from torch_geometric.loader import DataLoader

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from src.data.preprocessing.preprocess_utils import load_data_from_hdf5
from network.network import GraphQA


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config_tiny.yml')
    
    test = load_data_from_hdf5(config, 'test')
    model = GraphQA(conf=OmegaConf.create({
        'encoder': {
            'out_edge_feats': 64,
            'out_node_feats': 128,
        },
        'mp': {
            'out_edge_feats': 16,
            'out_node_feats': 64,
            'layers': 6,
            'in_global_feats': 512,
            'out_global_feats': 1,
            'dropout': 0.2,
            'batch_norm': False,
            'scatter': 'mean',
        }
    }))

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(100):
        model.train()
        total_loss = 0
        loader = DataLoader(test, batch_size=16)
        for data in loader:
            optimizer.zero_grad()
            x, edge_index, edge_attr, batch, y = model.prepare(data)
            out = model(x, edge_index, edge_attr, batch)
            loss = criterion(out, y) 
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        average_loss = total_loss / len(loader)
        print(f"Epoch {epoch + 1}, Loss: {average_loss:.4f}")
