import os
import pytorch_lightning as pl
from torch_geometric.loader import DataLoader

from ..data.preprocessing.hdf5_utils import load_data_from_hdf5
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig


class GRNDataModule(pl.LightningDataModule):
    def __init__(
        self, 
        config: RnaquanetConfig
    ):
        super().__init__()
        self.config = config
        self.batch_size = config.network.batch_size
        self.num_workers = config.network.num_workers
        self.shuffle_train = config.network.shuffle_train
        self.shuffle_val = config.network.shuffle_val
        self.shuffle_test = config.network.shuffle_test

    def prepare_data(self):
        self.train_data = load_data_from_hdf5(os.path.join(self.config.data.path, self.config.name, 'train.h5'))
        self.val_data = load_data_from_hdf5(os.path.join(self.config.data.path, self.config.name, 'val.h5'))
        self.test_data = load_data_from_hdf5(os.path.join(self.config.data.path, self.config.name, 'test.h5'))

    def train_dataloader(self):
        return DataLoader(self.train_data, batch_size=self.batch_size, shuffle=self.shuffle_train, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.val_data, batch_size=self.batch_size, shuffle=self.shuffle_val, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.test_data, batch_size=self.batch_size, shuffle=self.shuffle_test, num_workers=self.num_workers)
