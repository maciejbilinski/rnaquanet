from dataclasses import dataclass
import yaml

@dataclass
class ConfigDataDownload:
    name: str
    url: str
    archive_ext: str
    test_folder: str
    train_folder: str
    rmsd_csv_file_path: str
    rmsd_csv_delimiter: str
    rmsd_column_name: str
    csv_structure_column_name: str
    structure_colume_ext: str

@dataclass
class ConfigDataDownloadPreprocessed:
    train_url: str
    test_url: str

@dataclass
class ConfigDataFeatures:
    atom_for_distance_calculations: str
    max_euclidean_distance: str

@dataclass
class ConfigData:
    download: ConfigDataDownload
    features: ConfigDataFeatures
    download_preprocessed: ConfigDataDownloadPreprocessed

    def __init__(self, data: dict):
        self.download = ConfigDataDownload(**data['download'])
        self.features = ConfigDataFeatures(**data['features'])
        self.download_preprocessed = ConfigDataDownloadPreprocessed(**data['download_preprocessed'])

@dataclass
class ConfigNetworkEncoder:
    dropout: float
    batch_norm: bool
    in_edge_feats: int
    out_edge_feats: int
    in_node_feats: int
    out_node_feats: int

@dataclass
class ConfigNetworkMessagePassing:
    layers: int
    dropout: float
    batch_norm: bool
    scatter: str
    out_edge_feats: int
    out_node_feats: int
    in_global_feats: int
    out_global_feats: int
    layer_sizes_func: str

@dataclass
class ConfigNetworkReadout:
    layers: int
    out_feats: int
    layer_sizes_func: str

@dataclass
class ConfigNetwork:
    encoder: ConfigNetworkEncoder
    message_passing: ConfigNetworkMessagePassing
    readout: ConfigNetworkReadout

    def __init__(self, data: dict):
        self.encoder = ConfigNetworkEncoder(**data['encoder'])
        self.message_passing = ConfigNetworkMessagePassing(**data['message_passing'])
        self.readout = ConfigNetworkReadout(**data['readout'])

class RnaquanetConfig:
    data: ConfigData
    network: ConfigNetwork

    def __init__(self, path: str):
        with open(path, "r") as stream:
            try:
                result = yaml.safe_load(stream)
                self.data = ConfigData(result['data'])
                self.network = ConfigNetwork(result['network'])
            except yaml.YAMLError as exc:
                e = Exception(exc)
                e.add_note('Cannot load config file')
                raise e
            except TypeError as exc:
                e = Exception(exc)
                e.add_note('Config file has incorrect structure')
                raise e