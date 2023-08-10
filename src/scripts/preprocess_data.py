import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from data.preprocess_utils import filter_file, extract_features, get_data_lists, save_data_to_hdf5


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config.yml')
    
    LIST_OF_FILES = [
        'test/1a4d_S_000002_minimize_001.pdb',
        'train/1csl_S_000023_minimize_005.pdb',
        'test/1a4d_S_000036_minimize_006.pdb',
        'test/1a4d_S_000121_minimize_001.pdb'
    ]
        
    # TODO: argparser
    filter_file(LIST_OF_FILES, config)
    extract_features(LIST_OF_FILES, config)
    data_lists = get_data_lists(LIST_OF_FILES, config)

    # for key in data_lists:
    #     save_data_to_hdf5(config, key, data_lists[key])
