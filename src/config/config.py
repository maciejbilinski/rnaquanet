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

@dataclass
class ConfigData:
    download: ConfigDataDownload
    features: ConfigDataFeatures
    download_preprocessed: ConfigDataDownloadPreprocessed

    def __init__(self, data: dict):
        self.download = ConfigDataDownload(**data['download'])
        self.features = ConfigDataFeatures(**data['features'])
        self.download_preprocessed = ConfigDataDownloadPreprocessed(**data['download_preprocessed'])

class RnaquanetConfig:
    data: ConfigData

    def __init__(self, path: str):
        with open(path, "r") as stream:
            try:
                result = yaml.safe_load(stream)
                self.data = ConfigData(result['data'])
            except yaml.YAMLError as exc:
                e = Exception(exc)
                e.add_note('Cannot load config file')
                raise e
            except TypeError as exc:
                e = Exception(exc)
                e.add_note('Config file has incorrect structure')
                raise e