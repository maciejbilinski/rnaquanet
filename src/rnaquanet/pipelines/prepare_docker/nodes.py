import os
import shutil
import tarfile
import requests
import subprocess
from tqdm import tqdm

class DockerServiceDoesNotStartedError(Exception):
    """Exception raised when docker service does not started
    """

    def __init__(self):
        super().__init__('Is your docker service started? Type "sudo systemctl start docker" to solve the problem')

def download_structure_descriptor_docker_file(url: str, path: str) -> None:
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

def add_docker_image(path: str) -> None:
    """Add docker image

    Args:
        path: directory where docker archive is stored
    Returns:
        None
    """
    if os.path.exists('/var/run/docker.pid'):
        s=subprocess.Popen(['docker','load','--input',os.path.join(path, 'docker_image.tar')], stdout=subprocess.PIPE)
        s.wait()
    else:
        raise DockerServiceDoesNotStartedError
