import glob
import os

from config.config import RnaquanetConfig
from config.custom_types import PathType

class InputsConfig:
    """
    Resolves input files based on configuration file.

    Parameters:
    - config - rnaquanet YML config file

    Members:
    - ALL_FILES - contains all files within 'train' and 'test' subdirs
    - TRAIN_FILES - contains files within 'train' subdir
    - TEST_FILES - contains files within 'test' subdir
    """
    def __init__(self, config: RnaquanetConfig) -> None:
        __download_subdir = config.data.download.name

        self.ALL_FILES = [InputsConfig.__get_name_from_path(filepath)
                          for filepath in glob.glob(f'data/{__download_subdir}/archive/**/*.pdb', recursive=True)]
        """Contains all files (data/[...]/archive/**/*.pdb)"""
        
        self.TRAIN_FILES = [InputsConfig.__get_name_from_path(filepath)
                            for filepath in glob.glob(f'data/{__download_subdir}/archive/train/*.pdb', recursive=True)]
        """Contains 'train' files (data/[...]/archive/train/*.pdb)"""
        
        self.TEST_FILES = [InputsConfig.__get_name_from_path(filepath)
                           for filepath in glob.glob(f'data/{__download_subdir}/archive/test/*.pdb', recursive=True)]
        """Contains 'test' files (data/[...]/archive/test/*.pdb)"""
    

    def __get_name_from_path(path: PathType) -> str:
        """
        Returns the filename and the last directory path
        """
        return os.path.join(os.path.basename(os.path.dirname(path)), os.path.basename(path))
