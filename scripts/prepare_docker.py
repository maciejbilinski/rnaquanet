import argparse
import os
import requests
import subprocess

from rnaquanet.utils.docker_handler import check_docker_image
from rnaquanet.utils.docker_handler import check_docker_run
from tqdm import tqdm
from CONFIG import prepare_docker as params
from CONFIG import change_dir


def download_structure_descriptor_docker_file(url: str, path: str,*args) -> bool:
    """Download docker image

    Args:
        url: URL to docker image.
        path: directory where archive will be saved
    Returns:
        None
    """
    if not os.path.exists(os.path.join(path, 'docker_image.tar')):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(os.path.join(path, 'docker_image.tar'), 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

    return True

def add_docker_image(path: str, raise_on_error: bool,*args) -> bool:
    """Add docker image

    Args:
        path: directory where docker archive is stored
    Returns:
        None
    """
    if not check_docker_image('describe_structure',False):
        if raise_on_error:
            check_docker_run()
        s=subprocess.Popen(['docker','load','--input',os.path.join(path, 'docker_image.tar')], stdout=subprocess.PIPE, text=True)
        s.wait()
        return check_docker_image('describe_structure',raise_on_error)
    return True


if __name__ == '__main__':
    change_dir('..')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--structure-descriptor-docker-image',
        default=params.structure_descriptor_docker_image
    )
    parser.add_argument(
        '--docker-image-path',
        default=params.docker_image_path
    )
    args = parser.parse_args()

    download_structure_descriptor_docker_file(args.structure_descriptor_docker_image, args.docker_image_path)
    add_docker_image(args.docker_image_path, params.raise_on_error)
    
