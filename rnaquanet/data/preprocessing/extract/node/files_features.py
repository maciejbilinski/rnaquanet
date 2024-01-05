import os
import pandas as pd
from typing import Literal
from rnaquanet.utils.custom_types import PathType
from rnaquanet.utils.rnaquanet_config import RnaquanetConfig


def get_features_from_file(config: RnaquanetConfig, feature_directory_path: PathType,
                                file_type: Literal['bon', 'ang', 'atr'],
                                exclude_columns: list[str] = ['Chain', 'ResNum', 'iCode', 'Name']
                                ) -> pd.DataFrame:
    """
    Get features from a given file type.

    Args:
    - config - Rnaquanet config file
    - feature_directory_path - absolute path directory containing feature files
    - file_type - type of file with sample's features
    (supported: bon, ang, atr)
    - exclude_columns - list of columns which should be excluded

    Returns:
    - Pandas dataframe with features from chosen sample and file type
    """
    nan_behavior = config.data.features.nan_behavior.file_type
    
    df = pd.read_csv(os.path.join(feature_directory_path, f"{os.path.splitext(os.path.basename(feature_directory_path))[0]}.{file_type}"), sep='\t', index_col=False)
    df.reset_index(drop=True, inplace=True)
    df.drop(columns=exclude_columns, inplace=True)
    df = df.add_prefix(f'{file_type}_')

    if nan_behavior == 'col':
        # remove columns with empty values
        df = df.loc[:, ~df.isin(['-']).any()]
    if nan_behavior == 'row':
        # remove rows with empty values
        df = df[~df.isin(['-']).any(axis=1)]
    else:
        if nan_behavior:
            # replace empty values with value
            df.replace({'-': nan_behavior}, inplace=True)
        else:
            # do nothing
            df.replace({'-': 'NaN'}, inplace=True)
        
    return df
