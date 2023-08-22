from data.preprocess_utils import filter_file, extract_features, get_data_lists, save_data_to_hdf5, load_data_from_hdf5
from config.os import change_dir
from config.config import RnaquanetConfig
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


if __name__ == '__main__':
    change_dir('../../data/test')
    config = RnaquanetConfig('config.yml')

    LIST_OF_FILES = [
        'test/1a4d_S_000002_minimize_001.pdb',
        'train/1csl_S_000023_minimize_005.pdb',
        'test/1a4d_S_000036_minimize_006.pdb',
        'test/1a4d_S_000121_minimize_001.pdb'
    ]

    filter_file(LIST_OF_FILES, config)
    extract_features(LIST_OF_FILES, config)
    data_lists = get_data_lists(LIST_OF_FILES, config)
    
    # test multiple file feature extranction
    assert str(data_lists) == """{'test': [Data(x=[41, 96], edge_index=[2, 360], edge_attr=[360, 2], y=7.2129998207092285), Data(x=[41, 96], edge_index=[2, 386], edge_attr=[386, 2], y=6.576000213623047), Data(x=[41, 96], edge_index=[2, 378], edge_attr=[378, 2], y=14.145999908447266)], 'train': [Data(x=[28, 96], edge_index=[2, 360], edge_attr=[360, 2], y=13.97599983215332)]}"""

    LIST_OF_FILES = [
        'train/1csl_S_000023_minimize_005.pdb',
    ]
    
    filter_file(LIST_OF_FILES, config)
    extract_features(LIST_OF_FILES, config)
    data_lists = get_data_lists(LIST_OF_FILES, config)
    
    # test `get_data_lists` correctly avoiding files that were not provided in list of files
    assert str(data_lists) == """{'train': [Data(x=[28, 96], edge_index=[2, 360], edge_attr=[360, 2], y=13.97599983215332)]}"""

    for key in data_lists:
        save_data_to_hdf5(config, key, data_lists[key])
        
    # test if data was correctly saved and loaded from hdf5
    assert str(load_data_from_hdf5(config, 'train.h5')) == data_lists['train']
