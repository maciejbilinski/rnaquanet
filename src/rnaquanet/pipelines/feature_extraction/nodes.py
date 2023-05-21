import glob
import subprocess
import shutil
import os
from pathlib import Path
"""
This is a boilerplate pipeline 'feature_extraction'
generated using Kedro 0.18.8
"""

def extract_features_from_structure_file_using_docker(train: bool,structure_descriptor_params) -> None:
    """Extract features from files

    Args:
        train: is it training.
    Returns:
        None
    """
    if train:
        source_directory=os.path.join('data/02_intermediate','train')
        destination_directory=os.path.join('data/03_primary','train')
    else:
        source_directory=os.path.join('data/02_intermediate','test')
        destination_directory=os.path.join('data/03_primary','train')
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
        os.mkdir(destination_directory)
    for feature_file in list(set(glob.glob(source_directory+'/*.*')) - set(glob.glob(os.path.join(source_directory,'*.pdb')))):
        shutil.move(feature_file,destination_directory)

