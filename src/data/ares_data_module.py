import pytorch_lightning as pl
from torch_geometric.loader import DataLoader

from .preprocess_utils import load_data_from_hdf5

class AresDataModule(pl.LightningDataModule):
    def __init__(self, config, batch_size=1000, num_workers=1, shuffle_train=True, shuffle_val=False):
        super().__init__()
        self.config = config
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle_train = shuffle_train
        self.shuffle_val = shuffle_val

    def prepare_data(self):
        self.train_data = load_data_from_hdf5(self.config, 'train')
        self.val_data = load_data_from_hdf5(self.config, 'test')
        # temp = self.train_data [:2000]
        # self.train_data [:2000] = self.val_data[:2000]
        # self.val_data[:2000] = temp

    def train_dataloader(self):
        return DataLoader(self.train_data[4000:], batch_size=self.batch_size, shuffle=self.shuffle_train, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.train_data[:4000], batch_size=self.batch_size, shuffle=self.shuffle_val, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.val_data, batch_size=self.batch_size, shuffle=self.shuffle_val, num_workers=self.num_workers)
