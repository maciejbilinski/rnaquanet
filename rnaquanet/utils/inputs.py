import glob
import os

from .rnaquanet_config import RnaquanetConfig

class InputsConfig:
    """
    Resolves input files based on configuration file.

    Parameters:
    - config - rnaquanet YML config file

    Members:
    - ALL_FILES - contains all files within 'train' and 'test' subdirs
    - TRAIN_FILES - contains files within 'train' subdir
    - VAL_FILES - contains files within 'val' subdir
    - TEST_FILES - contains files within 'test' subdir
    """
    def __init__(self, config: RnaquanetConfig) -> None:
        __download_subdir = config.name

        self.ALL_FILES = glob.glob(f'{config.data.path}/{__download_subdir}/archive/**/*.pdb', recursive=True)
        """Contains all files (data/[...]/archive/**/*.pdb)"""
        
        self.TRAIN_FILES = glob.glob(f'{config.data.path}/{__download_subdir}/archive/train/*.pdb', recursive=True)
        """Contains 'train' files (data/[...]/archive/train/*.pdb)"""

        self.VAL_FILES = glob.glob(f'{config.data.path}/{__download_subdir}/archive/train/*.pdb', recursive=True)
        """Contains 'val' files (data/[...]/archive/val/*.pdb)"""
        
        self.TEST_FILES = glob.glob(f'{config.data.path}/{__download_subdir}/archive/test/*.pdb', recursive=True)
        """Contains 'test' files (data/[...]/archive/test/*.pdb)"""

