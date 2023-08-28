import argparse
from multiprocessing import Pool
import sys
import os
import glob
import multiprocessing as mp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tqdm import tqdm
from rnaquanet import get_base_dir
from src.data.preprocessing.hdf5_utils import concat_hdf5_files
from src.config.os import change_dir
from src.config.config import RnaquanetConfig
from src.config.prepare_target_set import read_target_csv
from src.data.preprocessing.preprocess_utils import process_structure, process_structure_f
from src.config.inputs import InputsConfig


parser = argparse.ArgumentParser(
                usage="%(prog)s",
                prog='RNAquanet',
                description='Run input processing',
                )
parser.add_argument('-d', '--directory', help="Structure store directory, absolute path")
parser.add_argument('-r', '--redis-support',action="store_true")


if __name__ == '__main__':
    change_dir('../..')

    config = RnaquanetConfig('config_tiny.yml')
    args = parser.parse_args()
     
    
    if config.data.production:
        if args.directory:
            for structure in glob.glob(args.directory+'/*.pdb'):
                process_structure(structure,config,'test',None)
            os.makedirs(os.path.join(get_base_dir(), 'data',config.data.download.name), exist_ok=True)   
            concat_hdf5_files(
                    os.path.join(get_base_dir(), 'data',config.data.download.name+'.h5'),
                    glob.glob(os.path.join(get_base_dir(), 'data','h5',config.data.download.name,'*.h5')))
        elif args.pdb_file:
            process_structure(args.pdb_file, config,'test',None)
    
    else:
        df = read_target_csv(config.data)
        with Pool(mp.cpu_count()) as pool:
            for _ in tqdm(enumerate(pool.imap_unordered(process_structure_f, [[structure,config,'test',df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target']] for structure in InputsConfig(config).TEST_FILES])),
                        total=len(InputsConfig(config).TEST_FILES), unit='f'):
                continue

        with Pool(mp.cpu_count()) as pool:
            for _ in tqdm(enumerate(pool.imap_unordered(process_structure_f, [[structure,config,'train',df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target']] for structure in InputsConfig(config).TRAIN_FILES])),
                        total=len(InputsConfig(config).TRAIN_FILES), unit='f'):
                continue

        os.makedirs(os.path.join(get_base_dir(), 'data',config.data.download.name), exist_ok=True)
        concat_hdf5_files(
                os.path.join(get_base_dir(), 'data',config.data.download.name,'test.h5'),
                glob.glob(os.path.join(get_base_dir(), 'data','h5',config.data.download.name,'test','*.h5')))
        concat_hdf5_files(
                os.path.join(get_base_dir(), 'data',config.data.download.name,'train.h5'),
                glob.glob(os.path.join(get_base_dir(), 'data','h5',config.data.download.name,'train','*.h5')))
