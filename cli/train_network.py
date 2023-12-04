import os
import torch
import pytorch_lightning as pl
from time import time_ns
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from rnaquanet.network.grn_data_module import GRNDataModule
from utils.parser import RnaquanetParser
from pytorch_lightning.loggers import TensorBoardLogger

if __name__ == '__main__':
    parser = RnaquanetParser(description="Train network")
    config = parser.get_config()

    torch.set_float32_matmul_precision('high')

    data = GRNDataModule(config)
    data.prepare_data()

    path = os.path.join(config.network.model_output_path, str(time_ns()))
    os.makedirs(path, exist_ok=False)

    model = GraphRegressionNetwork(config)
    trainer = pl.Trainer(max_epochs=config.network.max_epochs, log_every_n_steps=1, callbacks=[
        EarlyStopping('val_loss'),
        ModelCheckpoint(dirpath=path, save_top_k=3, monitor='val_loss'),
    ], logger=TensorBoardLogger("tb_logs", name="RnaQALightning"))
    trainer.fit(model, data)
    trainer.save_checkpoint(os.path.join(path, 'final.cpkt'))

