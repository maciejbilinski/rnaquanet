from dataclasses import dataclass
from .custom_types import NanBehaviorType
import os

@dataclass
class ConfigDataDownload:
    url: str | bool
    archive_ext: str

    train_folder: str
    val_folder: str
    test_folder: str

    train_csv: str
    val_csv: str
    test_csv: str

    csv_delimiter: str
    csv_rmsd_column_name: str
    csv_structure_column_name: str

@dataclass
class ConfigDataDownloadPreprocessed:
    train_url: str
    val_url: str
    test_url: str

@dataclass
class ConfigDataFeaturesNanBehavior:
    ang: NanBehaviorType
    atr: NanBehaviorType
    bon: NanBehaviorType
    tor: NanBehaviorType

@dataclass
class ConfigDataFeatures:
    atom_for_distance_calculations: str
    max_euclidean_distance: str
    regenerate_features_when_exists: bool
    nan_behavior: ConfigDataFeaturesNanBehavior

@dataclass
class ConfigData:
    path: str
    download: ConfigDataDownload
    download_preprocessed: ConfigDataDownloadPreprocessed
    features: ConfigDataFeatures
    def __init__(self, data: dict):
        self.path = os.path.join(os.getcwd(), data['path'])
        self.download = ConfigDataDownload(**data['download'])
        self.features = ConfigDataFeatures(**data['features'])
        self.download_preprocessed = ConfigDataDownloadPreprocessed(**data['download_preprocessed'])

@dataclass
class ConfigNetwork:
    model_output_path: str
    hidden_dim: int
    layer_type: int
    num_of_layers: int
    num_of_node_features: int
    batch_norm: bool
    gat_dropout: float
    lr: float
    weight_decay: float
    scheduler_step_size: int
    scheduler_gamma: float
    batch_size: int
    num_workers: int
    shuffle_train: bool
    shuffle_val: bool
    shuffle_test: bool
    max_epochs: int

    def __init__(self, data: dict):
        self.model_output_path = os.path.join(os.getcwd(), data['model_output_path'])
        self.hidden_dim = data['hidden_dim']
        self.layer_type = data['layer_type']
        self.num_of_layers = data['num_of_layers']
        self.num_of_node_features = data['num_of_node_features']
        self.batch_norm = data['batch_norm']
        self.gat_dropout = data['gat_dropout']
        self.lr = data['lr']
        self.weight_decay = data['weight_decay']
        self.scheduler_step_size = data['scheduler_step_size']
        self.scheduler_gamma = data['scheduler_gamma']
        self.batch_size = data['batch_size']
        self.num_workers = data['num_workers']
        self.shuffle_train = data['shuffle_train']
        self.shuffle_val = data['shuffle_val']
        self.shuffle_test = data['shuffle_test']
        self.max_epochs = data['max_epochs']