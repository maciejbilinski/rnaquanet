import glob
import subprocess
import shutil
import os
import re
from typing import Tuple
import pandas as pd
from pathlib import Path
from Bio.PDB import PDBParser
from rnapolis import parser, annotator, tertiary

"""
This is a boilerplate pipeline 'feature_extraction'
generated using Kedro 0.18.8
"""

def extract_features_from_structure_file_using_docker(train: bool, paths, structure_descriptor_params) -> None:
    """Extract features from files
    Args:
        train: is it training.
        structure_descriptor_params: params for structure descriptor
    Returns:
        None
    """
    if train:
        source_directory=os.path.join(paths['src'],'train')
        destination_directory=os.path.join(paths['dest'],'train')
    else:
        source_directory=os.path.join(paths['src'],'test')
        destination_directory=os.path.join(paths['dest'],'test')
    for structure_file in glob.glob(os.path.join(source_directory,'*.pdb')):
        s=subprocess.Popen(['docker',
                            'run',
                            '--rm',
                            '-v',
                            str(Path().absolute())+'/'+source_directory+':/tmp',
                            'describe_structure:latest',
                            '/tmp/'+structure_file.split('/')[-1],
                            str(structure_descriptor_params['atom_for_distance_calculations']),
                            str(structure_descriptor_params['max_euclidean_distance'])],
                        stdout=subprocess.PIPE)
        s.wait()
    if not os.path.exists(destination_directory):
        os.removedirs(destination_directory)
        os.mkdir(destination_directory)

    for feature_file in list(set(glob.glob(source_directory+'/*.*')) - set(glob.glob(os.path.join(source_directory,'*.pdb')))):
        shutil.move(feature_file,destination_directory)

def generate_features(paths, score_file_path:str)-> Tuple:
    """Extract features from files
    Args:
        score_file_path: path to score.sc file 
    Returns:
        train_df, test_df: extracted data for data catalogs
    """
    train_df=pd.DataFrame()
    test_df =pd.DataFrame()
    for train in [True,False]:
        if train:
            source_directory=os.path.join(paths['src'],'train')
        else:
            source_directory=os.path.join(paths['src'],'test')

        extracted_structures = set([filename.split('/')[-1].split('.')[0] for filename in glob.glob(source_directory+'/*.pdb')])
        column_to_save=['description','new_rms']

        df = pd.read_csv(score_file_path,sep=' ')
        df.drop(list(set(df.columns.values.tolist())-set(column_to_save)), axis=1, inplace=True)
        df['description']=df['description'].str.replace('.pdb','',regex=False)
        df.drop(df[~df['description'].isin(extracted_structures)].index, inplace=True)

        pdb_parser = PDBParser(QUIET=True)
        sequences=[]
        pairings=[]

        for index, row in df.iterrows():
            structure_pdb_path = os.path.join(str(Path().absolute()),source_directory,row['description']+'.pdb')
            structure_pdb = pdb_parser.get_structure("structure", structure_pdb_path)
            
            for model in structure_pdb:
                temp_seq=[]
                for chain in model:
                    temp_seq.append(''.join([re.sub(r'[^ATGCU]','',residue.resname) for residue in chain]))
                sequences.append(''.join(temp_seq))
            
            with open(os.path.join(str(Path().absolute()),source_directory,row['description']+'.pdb'),'r') as f:
                    structure3d = parser.read_3d_structure(f)
                    structure2d = annotator.extract_secondary_structure(
                        structure3d)
                    mapping = tertiary.Mapping2D3D(structure3d, structure2d, False)
                    temp=[]
                    for index,row in enumerate(mapping.dot_bracket.split('\n')):
                        if index%3 == 2:
                            temp.append(row)
                    pairings.append(''.join(temp))

        df['base_pairing']=pairings
        df['sequence']=sequences
        df = df.reset_index()
        df.drop('index',axis=1,inplace=True)
        if train:
            train_df=df.copy()
        else:
            test_df=df.copy()

    return train_df,test_df

