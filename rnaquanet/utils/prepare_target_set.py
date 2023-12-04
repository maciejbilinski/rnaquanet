
import os
import pandas as pd

from .rnaquanet_config import RnaquanetConfig


def read_target_csv(config: RnaquanetConfig, dataset: str):        
    
    # Structure CSV
    columns_to_save = [config.data.download.csv_rmsd_column_name, config.data.download.csv_structure_column_name]      
    df = pd.read_csv(os.path.join(config.data.path, config.name, 'archive', f'{dataset}.csv'), sep=config.data.download.csv_delimiter)

    # Drop all columns which are not in columns_to_save
    df.drop(list(set(df.columns.values.tolist()) - set(columns_to_save)), axis=1, inplace=True)
    df[config.data.download.csv_structure_column_name] = df[config.data.download.csv_structure_column_name].str.replace('.pdb', '', regex=False)

    # Drop all rows which do not match with processed filenames (file_names_without_ext)
    df.rename(columns={
        config.data.download.csv_rmsd_column_name: 'target', 
        config.data.download.csv_structure_column_name: 'description'
    }, inplace=True)
    
    return df