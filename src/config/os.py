import os
from .custom_types import PathType

def change_dir(directory: PathType) -> None:
    """
    Change dir relative to file

    Args:
    - directory: dir relative to file; should specify the root dir of the
    project (where data directory is present)
    """
    relative_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))
    os.chdir(relative_dir)
    