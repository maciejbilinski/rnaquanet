import os
import pandas as pd
from typing import Literal
from src.config.custom_types import PathType


def get_features_from_file(feature_directory_path: PathType, file_type: Literal['bon', 'ang', 'atr'],
                                nan_replacement: float = 0.0,
                                exclude_columns: list[str] = ['Chain', 'ResNum', 'iCode', 'Name']
                                ) -> pd.DataFrame:
    """
    Get features from a given file type.

    Args:
    - feature_directory_path - absolute path directory containing feature files
    - file_type - type of file with sample's features
    (supported: bon, ang, atr)
    - nan_replacement - value representing a replacement for NaN values
    found
    - exclude_columns - list of columns which should be excluded

    Returns:
    - Pandas dataframe with features from chosen sample and file type
    """
    
    
    df = pd.read_csv(os.path.join(feature_directory_path, f"{os.path.splitext(os.path.basename(feature_directory_path))[0]}.{file_type}"), sep='\t')
    return (df.reset_index(drop=True)
            .drop(columns=exclude_columns)
            .replace('-', nan_replacement)
            .fillna(nan_replacement)
            .add_prefix(f'{file_type}_'))