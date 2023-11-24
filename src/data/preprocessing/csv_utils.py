import os
import pandas as pd


from src.config.config import  ConfigData
from src.config.custom_types import PathType


def save_features_to_csv(df: pd.core.frame.DataFrame, output_csv_name: PathType, config: ConfigData):
    """
    Save features from dataframe to csv. Used when multithreaded task saves results.

    Args:
    - df - dataframe to save 
    - output_csv_name - absolute path to save csv 
    - config - rnaquanet YML config file

    Returns:
    - None
   
    """
    df = df.reset_index()
    df.drop('index', axis=1, inplace=True)
    csv_path = os.path.join(config.processing_output.csv_path, f'{os.path.splitext(os.path.basename(output_csv_name))[0]}.csv')
    
    if not os.path.exists(csv_path):
        # If csv does not exist, create it
        df.to_csv(csv_path)
    else:
        # If csv already exists, replace/append only new data
        df_old = pd.read_csv(csv_path, index_col=0)
        for _, row in df.iterrows():
            # If row already exists, remove it and append the new row
            if row['description'] in df_old['description'].values:
                df_old.loc[df_old['description'] == row['description'], :] = row.to_frame().T

            else: 
                df_old = pd.concat([df_old, row.to_frame().T], ignore_index=True)
        
        df_old.to_csv(csv_path)