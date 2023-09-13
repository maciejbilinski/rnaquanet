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
    structure_column_ext: str

@dataclass
class ConfigDataDownloadPreprocessed:
    train_url: str
    test_url: str

@dataclass
class ConfigDataFeatures:
    atom_for_distance_calculations: str
    max_euclidean_distance: str
    regenerate_features_when_exists: bool

@dataclass
class ConfigDataPreprocessingOutput:
    csv_path: str
    h5_output: str

@dataclass
class ConfigData:
    download: ConfigDataDownload
    features: ConfigDataFeatures
    download_preprocessed: ConfigDataDownloadPreprocessed
    processing_output: ConfigDataPreprocessingOutput
    production:bool
    def __init__(self, data: dict):
        self.download = ConfigDataDownload(**data['download'])
        self.features = ConfigDataFeatures(**data['features'])
        self.download_preprocessed = ConfigDataDownloadPreprocessed(**data['download_preprocessed'])
        self.processing_output = ConfigDataPreprocessingOutput(**data['preprocessing_output'])
        self.production = data['production']

class RnaquanetConfig:
    data: ConfigData
    redis_accelerate: bool
    def __init__(self, path: str,redis_accelerate:bool=False):
        with open(path, "r") as stream:
            try:
                result = yaml.safe_load(stream)
                self.data = ConfigData(result['data'])
                self.redis_accelerate = redis_accelerate 
            except yaml.YAMLError as exc:
                e = Exception(exc)
                e.add_note('Cannot load config file')
                raise e
            except TypeError as exc:
                e = Exception(exc)
                e.add_note('Config file has incorrect structure')
                raise e