from omegaconf import OmegaConf
import pytorch_lightning as pl
from .rnaqa import RnaQA
import torch.nn as nn
from torch.optim import Adam

class RnaQALightning(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = RnaQA(conf=OmegaConf.create({
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
        self.criterion = nn.MSELoss()

    def forward(self, x, edge_index, edge_attr, batch):
        return self.model(x, edge_index, edge_attr, batch)

    def training_step(self, batch, batch_idx):
        x, edge_index, edge_attr, batch, y = self.model.prepare(batch)
        out = self(x, edge_index, edge_attr, batch)
        loss = self.criterion(out, y)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True, batch_size=len(batch))
        return loss

    def validation_step(self, batch, batch_idx):
        x, edge_index, edge_attr, batch, y = self.model.prepare(batch)
        out = self(x, edge_index, edge_attr, batch)
        loss = self.criterion(out, y)
        self.log("val_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True, batch_size=len(batch))
        return loss

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=1e-2)
        return optimizer