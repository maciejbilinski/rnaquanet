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
from data.ares_data_module import AresDataModule
from lightning.pytorch.loggers import TensorBoardLogger

if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config.yml')

    torch.set_float32_matmul_precision('high')
    

    model = RnaQALightning(config=config, lr=1e-3)
    data = AresDataModule(config, batch_size=32, num_workers=0)
    logger = TensorBoardLogger("tb_logs", name="RnaQALightning")

    checkpoint_callback = pl.callbacks.ModelCheckpoint(
        dirpath=f'checkpoints_{time.time()}',
        filename='{epoch}-{val_loss:.2f}',
        monitor='val_loss',
        mode='min'
    )

    early_stopping_callback = pl.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        mode='min'
    )

    trainer = pl.Trainer(
        max_epochs=100000,
        log_every_n_steps = 1,
        callbacks=[checkpoint_callback, early_stopping_callback],
        logger=logger
    )

    trainer.fit(model, data)