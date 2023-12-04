
import os
import glob
import pandas as pd

from src.config.config import ConfigData


def read_target_csv(config:ConfigData):

    path = os.path.join('data', config.download.name, 'preprocessing')
    filtered_path = os.path.join(path, 'filtered')
    # for subdir in os.listdir(os.path.join(path, 'features')):
    # Structure CSV
    columns_to_save = [config.download.rmsd_column_name, config.download.csv_structure_column_name]      
    df = pd.read_csv(os.path.join('data', config.download.name, 'archive', 'target.csv'), sep=config.download.rmsd_csv_delimiter)

    # Set of all *.pdb filenames without extensions

    # Drop all columns which are not in columns_to_save
    df.drop(list(set(df.columns.values.tolist()) - set(columns_to_save)), axis=1, inplace=True)
    df['description'] = df['description'].str.replace('.pdb', '', regex=False)

    # Drop all rows which do not match with processed filenames (file_names_without_ext)
    df.rename(columns={
        config.download.rmsd_column_name: 'target', 
        config.download.csv_structure_column_name: 'description'
    }, inplace=True)
    
    return df