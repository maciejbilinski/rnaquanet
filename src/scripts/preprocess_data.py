import argparse
import sys
import os
import glob
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.os import change_dir
from config.config import RnaquanetConfig
from config.prepare_target_set import read_target_csv
from data.preprocessing.preprocess_utils import process_structure
from config.inputs import InputsConfig


parser = argparse.ArgumentParser(
                usage="%(prog)s",
                prog='RNAquanet',
                description='Run input processing',
                )
parser.add_argument('-d', '--directory',name='directory', help="Structure store directory, absolute path")
parser.add_argument('-f', '--pdb-file',name='pdb')
parser.add_argument('-r', '--redis-support',name='redis')


if __name__ == '__main__':
    change_dir('../..')

    config = RnaquanetConfig('config_tiny.yml')
    args = parser.parse_args()


    if config.production:
        if args.d:
            for structure in glob.glob(args.d+'/*.pdb'):
                process_structure(structure,config,'test',None)
        elif args.f:
            process_structure(args.f,config,'test',None)
    
    else:
        df = read_target_csv(config)
        for structure in InputsConfig(config).TEST_FILES:
            process_structure(structure,config,'test',float(df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target']))
        for structure in InputsConfig(config).TRAIN_FILES:
            process_structure(structure,config,'train',float(df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target']))
