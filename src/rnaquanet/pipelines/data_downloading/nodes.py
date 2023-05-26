import os
import shutil
import tarfile
import requests
from tqdm import tqdm

from rnaquanet.utils.file_management import clear_catalog
def download_ares_archive(url: str, path: str,*args) -> bool:
    """Download ares archive

    Args:
        url: URL to ares dataset.
        path: directory where archive will be saved
    Returns:
        None
    """
    if not os.path.exists(os.path.join(path, 'archive.tar')):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(os.path.join(path, 'archive.tar'), 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

    return True

def extract_ares_archive(file_path: str, output_path: str,*args) -> bool:
    """Extract ares archive

    Args:
        file_path: directory where archive is saved
        output_path: directory where archive will be extracted
    Returns:
        None
    """
    clear_catalog(output_path) 
    source_dir = os.path.join(output_path, 'classics_train_val')
    with tarfile.open(os.path.join(file_path, 'archive.tar')) as tar:
        tar.extractall(output_path)
    target_dir = output_path
    

    file_names = os.listdir(source_dir)
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)

    shutil.rmtree(os.path.join(target_dir, 'lmdbs'))
    
    return True
