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
from itertools import product
import pandas as pd

if __name__ == '__main__':
    change_dir('../..')
    torch.set_float32_matmul_precision('high')
    
    config = RnaquanetConfig('config.yml')
    data = AresDataModule(config, batch_size=2000, num_workers=0)

    lr = [ 1e-3, 5e-4]
    batch_size = [100, 1000]
    encoder_dropout = [0, 0.2, 0.5]
    encoder_batch_norm = [True, False]
    encoder_out_edge_feats = [16, 256]
    encoder_out_node_feats = [64, 512]
    message_passing_layers = [3, 6, 18]
    message_passing_dropout = [0.2, 0.5]
    message_passing_batch_norm = [True, False]
    message_passing_out_edge_feats = [64, 128]
    message_passing_out_node_feats = [64, 256]
    message_passing_in_global_feats = [16, 256]
    message_passing_out_global_feats = [32, 512]
    readout_layers = [2, 6]
    readout_out_feats = [64, 256]

    combinations = list(product(
        lr, batch_size, 
        encoder_dropout, encoder_batch_norm, encoder_out_edge_feats, encoder_out_node_feats,
        message_passing_layers, message_passing_dropout, message_passing_batch_norm,
        message_passing_out_edge_feats, message_passing_out_node_feats,
        message_passing_in_global_feats, message_passing_out_global_feats,
        readout_layers, readout_out_feats
    ))
    df = pd.DataFrame(combinations, columns=[
        'lr', 'batch_size', 
        'encoder_dropout', 'encoder_batch_norm', 'encoder_out_edge_feats', 'encoder_out_node_feats',
        'message_passing_layers', 'message_passing_dropout', 'message_passing_batch_norm',
        'message_passing_out_edge_feats', 'message_passing_out_node_feats',
        'message_passing_in_global_feats', 'message_passing_out_global_feats',
        'readout_layers', 'readout_out_feats'
    ])
    attempts = 1
    for i in range(attempts):
        df[f'train_loss_{i+1}'] = np.nan
        df[f'val_loss_{i+1}'] = np.nan
    df['train_loss_mean'] = np.nan
    df['val_loss_mean'] = np.nan
    df.reset_index()
    df = df.sample(frac = 1)

    patience = 2

    dt = time.time()
    for index, row in df.iterrows():
        for i in range(attempts):
            data.batch_size = row['batch_size']

            config.encoder_dropout = row['encoder_dropout']
            config.encoder_batch_norm = row['encoder_batch_norm']
            config.encoder_out_edge_feats = row['encoder_out_edge_feats']
            config.encoder_out_node_feats = row['encoder_out_node_feats']

            config.message_passing_layers = row['message_passing_layers']
            config.message_passing_dropout = row['message_passing_dropout']
            config.message_passing_batch_norm = row['message_passing_batch_norm']
            config.message_passing_out_edge_feats = row['message_passing_out_edge_feats']
            config.message_passing_out_node_feats = row['message_passing_out_node_feats']
            config.message_passing_in_global_feats = row['message_passing_in_global_feats']
            config.message_passing_out_global_feats = row['message_passing_out_global_feats']

            config.readout_layers = row['readout_layers']
            config.readout_out_feats = row['readout_out_feats']

            model = RnaQALightning(
                config = config,
                lr = row['lr']
            )

            checkpoint_callback = pl.callbacks.ModelCheckpoint(
                dirpath=f'checkpoints_{dt}/{index}/{i}',
                filename='{epoch}-{val_loss:.2f}',
                monitor='val_loss',
                mode='min'
            )

            early_stopping_callback = pl.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=patience,
                mode='min'
            )

            trainer = pl.Trainer(
                max_epochs=100000,
                log_every_n_steps = 1,
                callbacks=[checkpoint_callback, early_stopping_callback]
            )
            

            trainer.fit(model, data)
            df.at[index, f'train_loss_{i+1}'] = trainer.logged_metrics['train_loss_epoch'].item()
            best_model = RnaQALightning.load_from_checkpoint(
                checkpoint_callback.best_model_path, 
                config = config,
                lr = row['lr']
            )
            df.at[index, f'val_loss_{i+1}'] = trainer.validate(model=best_model, datamodule=data, verbose=False)[0]['val_loss_epoch']

        df.at[index, 'val_loss_mean'] = np.mean([df.at[index, f'val_loss_{i+1}'] for i in range(attempts)])
        df.at[index, 'train_loss_mean'] = np.mean([df.at[index, f'train_loss_{i+1}'] for i in range(attempts)])
        df.to_csv(f'checkpoints_{dt}/result.csv')
    df.to_excel(f'checkpoints_{dt}/result.xlsx')

                    