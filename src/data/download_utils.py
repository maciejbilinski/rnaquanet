import os
import shutil
import tarfile
import requests
from tqdm import tqdm

from config.config import ConfigData, RnaquanetConfig

def download_archive(config: RnaquanetConfig):
    config = config.data.download
    path = os.path.join('data', config.name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    response = requests.get(config.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(os.path.join(path, f'archive.{config.archive_ext}'), 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

def extract_archive(config: RnaquanetConfig):
    config = config.data.download
    path = os.path.join('data', config.name)
    if os.path.exists(path):
        if len(os.listdir(path)) == 1:
            archive = os.path.join(path, f'archive.{config.archive_ext}')
            if os.path.exists(archive):
                if config.archive_ext in ['tar']:
                    path = os.path.join(path, 'archive')
                    os.makedirs(path)
                    train_path = os.path.join(path, 'train')
                    test_path = os.path.join(path, 'test')
                    if config.archive_ext == 'tar':
                        tmp = os.path.join(path, 'tmp')
                        with tarfile.open(archive) as tar:
                            tar.extractall(tmp)
                        os.rename(os.path.join(tmp, config.rmsd_csv_file_path), os.path.join(path, 'target.csv'))
                        os.rename(os.path.join(tmp, config.train_folder), train_path)
                        os.rename(os.path.join(tmp, config.test_folder), test_path)
                        shutil.rmtree(tmp)
                        return
                    # else other extensions
                else:
                    raise Exception(f'{config.archive_ext} format is not supported')
    raise Exception(f'Downloaded archive cannot be extracted. Call download_archive function first')

def download_preprocessed(config: RnaquanetConfig):
    config: ConfigData = config.data
    path = os.path.join('data', config.download.name)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    for url, name in [(config.download_preprocessed.train_url, 'train.h5'), (config.download_preprocessed.test_url, 'test.h5')]:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(os.path.join(path, name), 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()


