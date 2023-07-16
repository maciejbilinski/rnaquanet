

import glob
import subprocess
import shutil
import os
import re
from multiprocessing import Pool
import multiprocessing as mp
from typing import Tuple
import pandas as pd
from pathlib import Path
from Bio.PDB import PDBParser
from rnapolis import parser, annotator, tertiary
from tqdm import tqdm
from rnaquanet.utils.docker_handler import check_docker_image
from rnaquanet.utils.docker_handler import check_docker_run
from rnaquanet.utils.file_management import clear_catalog
from CONFIG import feature_extraction as params
from CONFIG import change_dir


"""
This is a boilerplate pipeline 'feature_extraction'
generated using Kedro 0.18.8
"""
def loop_function(structure_file_dict):
    s=subprocess.Popen(['docker',
            'run',
            '--rm',
            '-v',
            str(Path().absolute())+'/'+structure_file_dict[1]+':/tmp',
            'describe_structure:latest',
            '/tmp/'+structure_file_dict[0].split('/')[-1],
            str(structure_file_dict[2]['atom_for_distance_calculations']),
            str(structure_file_dict[2]['max_euclidean_distance'])],
        stdout=subprocess.PIPE)
    s.wait()
def extract_features_from_structure_file_using_docker(train: bool, paths, structure_descriptor_params,*args) -> None:
    """Extract features from files
    Args:
        train: is it training.
        structure_descriptor_params: params for structure descriptor
    Returns:
        None
    """
    check_docker_run()
    check_docker_image('describe_structure')
    if train:
        source_directory=os.path.join(paths['src'],'train')
        destination_directory=os.path.join(paths['dest'],'train')
    else:
        source_directory=os.path.join(paths['src'],'test')
        destination_directory=os.path.join(paths['dest'],'test')

    clear_catalog(destination_directory)
    progress_bar = tqdm(total=len(glob.glob(os.path.join(source_directory,'*.pdb'))))


    with Pool(mp.cpu_count()) as pool:
        for i, _ in enumerate(pool.imap_unordered(loop_function,
                                               [[structure_file,source_directory,structure_descriptor_params]
                                               for structure_file in glob.glob(os.path.join(source_directory,'*.pdb'))]),1):
            progress_bar.update(1)

    progress_bar.close()

    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)

    for feature_file in list(set(glob.glob(source_directory+'/*.*')) - set(glob.glob(os.path.join(source_directory,'*.pdb')))):
        shutil.move(feature_file,destination_directory)

    return True


def generate_features(paths, score_file_path:str,*args)-> Tuple:
    """Extract features from files
    Args:
        score_file_path: path to score.sc file 
    Returns:
        train_df, test_df: extracted data for data catalogs
    """
    train_df=pd.DataFrame()
    test_df =pd.DataFrame()
    for train in [False,True]:
        if train:
            source_directory=os.path.join(paths['src'],'train')
        else:
            source_directory=os.path.join(paths['src'],'test')

        extracted_structures = set([filename.split('/')[-1].split('.')[0].replace('_filtered','') for filename in glob.glob(source_directory+'/*.pdb')])
        column_to_save=['description','new_rms']
        print(extracted_structures)        
        df = pd.read_csv('data/03_filtered/scores.sc',sep=' ')
        df.drop(list(set(df.columns.values.tolist())-set(column_to_save)), axis=1, inplace=True)
        df['description']=df['description'].str.replace('.pdb','',regex=False)
        df.drop(df[~df['description'].isin(extracted_structures)].index, inplace=True)

        pdb_parser = PDBParser(QUIET=True)
        sequences=[]
        pairings=[]

        progress_bar = tqdm(total=len(df.index))
        for index, row in df.iterrows():
            structure_pdb_path = os.path.join(str(Path().absolute()),source_directory,row['description']+'_filtered'+'.pdb')
            structure_pdb = pdb_parser.get_structure("structure", structure_pdb_path)
            
            for model in structure_pdb:
                temp_seq=[]
                for chain in model:
                    temp_seq.append(''.join([re.sub(r'[^ATGCU]','',residue.resname) for residue in chain]))
                sequences.append(''.join(temp_seq))
            
            with open(os.path.join(str(Path().absolute()),source_directory,row['description']+'_filtered'+'.pdb'),'r') as f:
                    structure3d = parser.read_3d_structure(f)
                    structure2d = annotator.extract_secondary_structure(
                        structure3d)
                    mapping = tertiary.Mapping2D3D(structure3d, structure2d, False)
                    temp=[]
                    for index,row in enumerate(mapping.dot_bracket.split('\n')):
                        if index%3 == 2:
                            temp.append(row)
                    pairings.append(''.join(temp))

            progress_bar.update(1)
        progress_bar.close()
        df['base_pairing']=pairings
        df['sequence']=sequences
        df = df.reset_index()
        df.drop('index',axis=1,inplace=True)
        if train:
            train_df=df.copy()
        else:
            test_df=df.copy()

    return train_df,test_df


if __name__ == '__main__':
    change_dir('..')
    
    extract_features_from_structure_file_using_docker(True, params.path, params.structure_descriptor_params)
    extract_features_from_structure_file_using_docker(False, params.path, params.structure_descriptor_params)
    train_df, test_df = generate_features(params.path, params.score_file_path)
