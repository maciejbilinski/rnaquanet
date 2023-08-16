import sys
import os
import time
from omegaconf import OmegaConf
import torch
from torch_geometric.data import Data, Batch
import pytorch_lightning as pl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from network.rnaqa_lightning import RnaQALightning
from network.rnaqa_lightning import RnaQA
from data.ares_data_module import AresDataModule
from torch_geometric.nn import GCNConv
import torch.nn.functional as F
from torch_geometric.nn import global_mean_pool
from torch.nn import Linear
from torch.optim import Adam
import torch.nn as nn
from network.utils import extract_batch
import numpy as np

if __name__ == '__main__':
    change_dir('../..')

    torch.set_float32_matmul_precision('high')

    device = torch.device('cuda:0')
        
    config = RnaquanetConfig('config.yml')
    data = AresDataModule(config, batch_size=1024, num_workers=1)
    data.prepare_data()
    model = RnaQA(config=config).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    criterion = torch.nn.MSELoss().to(device)
    

    for epoch in range(10):
        print(f'epoch {epoch+1}')
        model.train()
        losses = []
        for batch in data.train_dataloader():
            optimizer.zero_grad()

            x, edge_index, edge_attr, batch, y = extract_batch(batch)
            out = model(x.to(device), edge_index.to(device), edge_attr.to(device), batch.to(device))
            
            loss = criterion(out, y.to(device))
            loss.backward()
            losses.append(loss.to(torch.device('cpu')).item())

            optimizer.step()
        print('train_loss', np.mean(losses))

        losses = []
        outputs = []
        with torch.no_grad():
            model.eval()
            for batch in data.val_dataloader():
                x, edge_index, edge_attr, batch, y = extract_batch(batch.to(device))
                out = model(x.to(device), edge_index.to(device), edge_attr.to(device), batch.to(device))
                loss = criterion(out, y.to(device))
                losses.append(loss.to(torch.device('cpu')).item())
                outputs.extend(out.to(torch.device('cpu')).tolist())
        print('val_loss', np.mean(losses))
        print('val_sd', np.std(outputs))
        


    