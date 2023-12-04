import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from data.download_utils import download_archive, extract_archive


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config_test.yml')
    download_archive(config)
    
    # TEST if `archive.tar` exists
    assert os.path.isfile(f'data/{config.data.download.name}/archive.tar')
    
    extract_archive(config)
    
    list_dir = os.listdir(f'data/{config.data.download.name}/archive')
    
    # TEST if `target.csv` exists
    assert 'target.csv' in list_dir
    
    # TEST if `train` and `test` directories exist
    assert 'train' in list_dir
    assert 'test' in list_dir
    
    # TEST whether both directories contain correct (i.e. all) number of files
    assert len(os.listdir(f'data/{config.data.download.name}/archive/train')) == 14000
    assert len(os.listdir(f'data/{config.data.download.name}/archive/test')) == 4000
    