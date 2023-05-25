import subprocess



class DockerServiceDoesNotStartedError(Exception):
    """Exception raised when docker service does not started
    """

    def __init__(self):
        super().__init__('Is your docker service started? Type "sudo systemctl start docker" to solve the problem')

class DockerImageNotFoundError(Exception):
    """Exception raised when docker service does not started
    """

    def __init__(self,image_name=''):
        super().__init__('Docker image \''+image_name+'\''+' not found. You just need to run \'prepare_docker\' pipeline')



def check_docker_run():
    s=subprocess.Popen(['docker','--version'], stdout=subprocess.PIPE, text=True)
    s.wait()
    if s.returncode != 0:
        raise DockerServiceDoesNotStartedError

def check_docker_image(image_name=''):
    s=subprocess.Popen(['docker','image','ls','|','grep','\''+image_name+'\''], stdout=subprocess.PIPE, text=True)
    s.wait()
    if image_name not in s.stdout.read():
        raise DockerImageNotFoundError(image_name) 

