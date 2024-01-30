import os
import shutil
import tarfile
import requests

from rnaquanet.utils.dialogs import ensure_directory_not_exist, ensure_file_not_exist
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig
from rnaquanet.utils.safe_print import safe_print
from rnaquanet.utils.safe_tqdm import SafeTqdm

def download_archive(config: RnaquanetConfig) -> None:
    """
    Downloads raw dataset.

    Args:
    - config - rnaquanet YML config file

    Returns:
    - None
    """
    if config.data.download.url == False:
        return

    path = os.path.join(config.data.path, config.name)

    config_download = config.data.download

    file_path = os.path.join(path, f'archive.{config_download.archive_ext}')

    ensure_file_not_exist(config, file_path)
    os.makedirs(path, exist_ok=True)

    response = requests.get(config_download.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    safe_print(config, f'Downloading raw {config.name} dataset...')
    with SafeTqdm(config, total=total_size, unit='iB', unit_scale=True) as progress_bar:
        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)


def extract_archive(config: RnaquanetConfig) -> None:
    """
    Extracts downloaded raw dataset.

    Args:
    - config - rnaquanet YML config file

    Returns:
    - None

    Exceptions:
    - if archive extension format is not supported
    - if there's no archive to extract
    """
    safe_print(config, f'Extracting downloaded {config.name} archive...')
    path = os.path.join(config.data.path, config.name)
    config_download = config.data.download
    if os.path.exists(path):
        archive = os.path.join(path, f'archive.{config_download.archive_ext}')
        if os.path.exists(archive):
            if config_download.archive_ext in ['tar', 'tar.gz']:
                path = os.path.join(path, 'archive')
                ensure_directory_not_exist(config, path)
                os.makedirs(path)
                tmp = os.path.join(path, 'tmp')
                if config_download.archive_ext == 'tar':
                    with tarfile.open(archive) as tar:
                        tar.extractall(tmp)
                elif config_download.archive_ext == 'tar.gz':
                    with tarfile.open(archive, 'r:gz') as tar:
                        tar.extractall(tmp)
                # else other extensions

                shutil.copyfile(os.path.join(tmp, config_download.train_csv), os.path.join(path, 'train.csv'))
                shutil.copyfile(os.path.join(tmp, config_download.val_csv), os.path.join(path, 'val.csv'))
                shutil.copyfile(os.path.join(tmp, config_download.test_csv), os.path.join(path, 'test.csv'))
                os.rename(os.path.join(tmp, config_download.train_folder), os.path.join(path, 'train'))
                os.rename(os.path.join(tmp, config_download.val_folder), os.path.join(path, 'val'))
                os.rename(os.path.join(tmp, config_download.test_folder), os.path.join(path, 'test'))
                shutil.rmtree(tmp)
                safe_print(config, 'Finished extracting!')
                return
            else:
                raise Exception(f'{config_download.archive_ext} format is not supported')
    raise Exception(f'Downloaded archive cannot be extracted. Call download_archive function first')


def download_preprocessed(config: RnaquanetConfig) -> None:
    """
    Downloads preprocessed h5 train and test files.

    Args:
    - config - rnaquanet YML config file

    Returns:
    - None
    """
    path = os.path.join(config.data.path, config.name)

    for url, name in [(config.data.download_preprocessed.train_url, 'train.h5'), (config.data.download_preprocessed.val_url, 'val.h5'), (config.data.download_preprocessed.test_url, 'test.h5')]:
        file_path = os.path.join(path, name)
        try:
            ensure_file_not_exist(config, file_path)
            os.makedirs(path, exist_ok=True)

            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            safe_print(config, f'Downloading preprocessed {name} file...')
            with SafeTqdm(config, total=total_size, unit='iB', unit_scale=True) as progress_bar:
                with open(file_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
        except Exception:
            pass
