import os
import torch
import pytorch_lightning as pl
from time import time_ns
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from rnaquanet.network.graph_regression_network import GraphRegressionNetwork
from rnaquanet.network.h5_graph_dataset import H5GraphDataset
from utils.parser import RnaquanetParser
from pytorch_lightning.loggers import TensorBoardLogger
from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    parser = RnaquanetParser(description="Train network")
    config = parser.get_config()

    torch.set_float32_matmul_precision('high')

    with H5GraphDataset(os.path.join('data', config.name, 'train.h5')) as train_data:
        with H5GraphDataset(os.path.join('data', config.name, 'val.h5')) as val_data:
            path = os.path.join(config.network.model_output_path, str(time_ns()))
            os.makedirs(path, exist_ok=False)

            model = GraphRegressionNetwork(config)
            trainer = pl.Trainer(max_epochs=config.network.max_epochs, log_every_n_steps=1, callbacks=[
                EarlyStopping('val_loss'),
                ModelCheckpoint(dirpath=path, save_top_k=3, monitor='val_loss'),
            ], logger=TensorBoardLogger("tb_logs", name="RnaQALightning"))
            trainer.fit(
                model, 
                train_dataloaders=DataLoader(train_data, batch_size=config.network.batch_size, shuffle=config.network.shuffle_train, num_workers=config.network.num_workers), 
                val_dataloaders=DataLoader(val_data, batch_size=config.network.batch_size, shuffle=config.network.shuffle_val, num_workers=config.network.num_workers), 
            )
            trainer.save_checkpoint(os.path.join(path, 'final.cpkt'))

