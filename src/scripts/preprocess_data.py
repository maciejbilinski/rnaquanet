import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from data.preprocess_utils import filter_files, extract_features, get_data_list, save_data_to_hdf5


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config.yml')
        
    filter_files(config)
    extract_features(config)
    data_lists = get_data_list(config)

    for key in data_lists:
        save_data_to_hdf5(config, key, data_lists[key])
