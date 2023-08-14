import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import RnaquanetConfig
from config.os import change_dir
from data.download_utils import download_preprocessed


if __name__ == '__main__':
    change_dir('../..')
    config = RnaquanetConfig('config.yml')
    download_preprocessed(config)
