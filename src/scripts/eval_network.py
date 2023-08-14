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

class GCN(pl.LightningModule):
    def __init__(self, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(96, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, 2*hidden_channels)
        self.conv3 = GCNConv(2*hidden_channels, 3*hidden_channels)
        self.conv4 = GCNConv(3*hidden_channels, 2*hidden_channels)
        self.conv5 = GCNConv(2*hidden_channels, hidden_channels)
        self.lin = Linear(hidden_channels, 1)
        self.criterion = nn.MSELoss()

    def forward(self, x, edge_index, batch):
        # 1. Obtain node embeddings 
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)
        x = x.relu()
        x = self.conv4(x, edge_index)
        x = x.relu()
        x = self.conv5(x, edge_index)

        # 2. Readout layer
        x = global_mean_pool(x, batch)  # [batch_size, hidden_channels]

        # 3. Apply a final classifier
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)
        
        return x
    
    def training_step(self, batch, batch_idx):
        x, edge_index, edge_attr, batch, y = self.prepare(batch)
        out = self(x, edge_index, batch).view(-1)
        loss = self.criterion(out, y)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True, batch_size=len(batch))
        return loss

    def validation_step(self, batch, batch_idx):
        x, edge_index, edge_attr, batch, y = self.prepare(batch)
        out = self(x, edge_index, batch).view(-1)
        loss = self.criterion(out, y)
        self.log("val_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True, batch_size=len(batch))
        return loss

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=1e-3)
        return optimizer

    @staticmethod
    def prepare(graphs: Batch):
        x = graphs.x
        edge_index = graphs.edge_index
        edge_attr = graphs.edge_attr
        batch = graphs.batch
        y = graphs.y

        return x, edge_index, edge_attr, batch, y


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config.yml')

    torch.set_float32_matmul_precision('high')
    
    model = GCN(hidden_channels=512)
    data = AresDataModule(config, batch_size=500, num_workers=1)
    checkpoint_callback = pl.callbacks.ModelCheckpoint(
        dirpath=f'checkpoints_{time.time()}',
        filename='{epoch}-{val_loss:.2f}',
        monitor='val_loss',
        mode='min'
    )

    early_stopping_callback = pl.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        mode='min'
    )

    trainer = pl.Trainer(
        max_epochs=1000000,
        log_every_n_steps = 1,
        callbacks=[checkpoint_callback, early_stopping_callback]
    )

    trainer.fit(model, data)
    model = model.to(torch.device('cpu'))
    data = AresDataModule(RnaquanetConfig('config_tiny.yml'), batch_size=1, num_workers=1)
    data.prepare_data()
    with torch.no_grad():
        model.eval()
        print('real \tnet')
        for batch in data.val_dataloader():
            x, edge_index, edge_attr, batch, y = model.prepare(batch)
            out = model(x, edge_index, batch)
            print("{:05.2f}".format(y.item()), '\t', "{:05.2f}".format(out.item()))

    