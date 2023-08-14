import pytorch_lightning as pl
from torch_geometric.loader import DataLoader

from .preprocess_utils import load_data_from_hdf5

class AresDataModule(pl.LightningDataModule):
    def __init__(self, config, batch_size=2000, num_workers=1):
        super().__init__()
        self.config = config
        self.batch_size = batch_size
        self.num_workers = num_workers

    def prepare_data(self):
        self.train_data = load_data_from_hdf5(self.config, 'train')
        self.test_data = load_data_from_hdf5(self.config, 'test')

    def train_dataloader(self):
        return DataLoader(self.train_data, batch_size=self.batch_size, shuffle=True, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.test_data, batch_size=self.batch_size, num_workers=self.num_workers)
