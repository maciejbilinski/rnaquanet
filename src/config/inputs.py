import glob
import os

from config.custom_types import PathType

def get_name_from_path(path: PathType) -> str:
    """
    Returns the filename and the last directory path
    """
    return os.path.join(os.path.basename(os.path.dirname(path)), os.path.basename(path))


# Contains all files within 'data/ares/archive' subdirectory
ALL_FILES = [get_name_from_path(filepath)
             for filepath in glob.glob('../../data/ares/archive/**/*.pdb', recursive=True)]

# 'data/ares/archive/train'
TRAIN_FILES = [get_name_from_path(filepath)
               for filepath in glob.glob('../../data/ares/archive/train/*.pdb', recursive=True)]

# 'data/ares/archive/test'
TEST_FILES = [get_name_from_path(filepath)
              for filepath in glob.glob('../../data/ares/archive/test/*.pdb', recursive=True)]

CUSTOM_FILE_LIST = [
    # Input PDB filenames located relative to 'data/ares/archive' 
    ...
]
