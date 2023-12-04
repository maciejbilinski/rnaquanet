import pytorch_lightning as pl
from .rnaqa import RnaQA
import torch.nn as nn
from torch.optim import Adam
from config.config import RnaquanetConfig
from .utils import extract_batch

class RnaQALightning(pl.LightningModule):
    def __init__(self, config: RnaquanetConfig, lr: float, weight_decay: float = 0.1):
        super().__init__()
        self.model = RnaQA(config)
        self.criterion = nn.SmoothL1Loss()
        self.lr = lr
        self.weight_decay = weight_decay

    def forward(self, x, edge_index, edge_attr, batch):
        return self.model(x, edge_index, edge_attr, batch)
    
    def custom_histogram_adder(self):
        # iterating through all parameters
        for name,params in self.named_parameters():
            self.logger.experiment.add_histogram(name,params,self.current_epoch)
             
    def training_step(self, batch, batch_idx):
        x, edge_index, edge_attr, batch, y = extract_batch(batch)
        out = self(x, edge_index, edge_attr, batch)
        loss = self.criterion(out, y)

        self.log("train_loss", loss, on_epoch=True, prog_bar=True, logger=None, batch_size=len(batch))
        return {
            # REQUIRED: It ie required for us to return "loss"
            "loss": loss,
            # optional for batch logging purposes
            "log": {"train_loss": loss},
        }

    def validation_step(self, batch, batch_idx):
        x, edge_index, edge_attr, batch, y = extract_batch(batch)
        out = self(x, edge_index, edge_attr, batch)
        loss = self.criterion(out, y)

        self.log("val_loss", loss, on_epoch=True, prog_bar=True, logger=None, batch_size=len(batch))
        return {
            # REQUIRED: It ie required for us to return "loss"
            "loss": loss,
            # optional for batch logging purposes
            "log": {"val_loss": loss},
        }

    def configure_optimizers(self):
        optimizer = Adam(self.model.parameters(), lr = self.lr, weight_decay=self.weight_decay)
        return optimizer