import os
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from rnaquanet.data.download_utils import download_archive, extract_archive

if __name__ == '__main__':
    config = RnaquanetConfig(os.path.join(os.path.dirname(__file__), 'config_test.yml'))
    download_archive(config)
    
    # TEST if `archive.tar` exists
    assert os.path.isfile(os.path.join(config.data.path, config.name, 'archive.tar'))
    
    extract_archive(config)
    
    list_dir = os.listdir(os.path.join(config.data.path, config.name, 'archive'))
    
    # TEST if `target.csv` exists
    assert 'target.csv' in list_dir
    
    # TEST if `train` and `test` directories exist
    assert 'train' in list_dir
    assert 'val' in list_dir
    assert 'test' in list_dir
    
    # TEST whether both directories contain correct (i.e. all) number of files
    assert len(os.listdir(os.path.join(config.data.path, config.name, 'archive', 'train'))) == 60
    assert len(os.listdir(os.path.join(config.data.path, config.name, 'archive', 'val'))) == 20
    assert len(os.listdir(os.path.join(config.data.path, config.name, 'archive', 'test'))) == 20
    