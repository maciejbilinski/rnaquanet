import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from data.preprocess_utils import filter_file, extract_features, get_data_lists, save_data_to_hdf5
from config.inputs import ALL_FILES as FILES


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config.yml')
    
    filter_file(FILES, config)
    extract_features(FILES, config)
    data_lists = get_data_lists(FILES, config)

    for key in data_lists:
        save_data_to_hdf5(config, key, data_lists[key])
