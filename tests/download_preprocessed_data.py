import os
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from rnaquanet.data.download_utils import download_preprocessed

if __name__ == '__main__':
    config = RnaquanetConfig(os.path.join(os.path.dirname(__file__), 'config_test.yml'))
    download_preprocessed(config)
    
    # TEST if `train.h5` exists
    assert os.path.isfile(os.path.join(config.data.path, config.name, 'train.h5'))
    # TEST if `val.h5` exists
    assert os.path.isfile(os.path.join(config.data.path, config.name, 'val.h5'))
    # TEST if `test.h5` exists
    assert os.path.isfile(os.path.join(config.data.path, config.name, 'test.h5'))

    # TODO: można przeprowadzić testy czy te pliki da się wczytać i czy zawierają dane w odpowiednich kształtach i ilościach
    