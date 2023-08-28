import argparse
import sys
import os
import glob
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from rnaquanet import get_base_dir
from src.data.preprocessing.hdf5_utils import concat_hdf5_files
from src.scripts.redis_pipeline import Task, TaskLevel, run
from src.config.os import change_dir
from src.config.config import RnaquanetConfig
from src.config.prepare_target_set import read_target_csv
from src.data.preprocessing.preprocess_utils import process_structure
from src.config.inputs import InputsConfig


parser = argparse.ArgumentParser(
                usage="%(prog)s",
                prog='RNAquanet',
                description='Run input processing',
                )
parser.add_argument('-d', '--directory', help="Structure store directory, absolute path")
# parser.add_argument('-f', '--pdb-file')
parser.add_argument('-r', '--redis-support',action="store_true")


if __name__ == '__main__':
    change_dir('../..')

    config = RnaquanetConfig('config_tiny.yml')
    args = parser.parse_args()
     
    if args.redis_support:
        df = read_target_csv(config.data)
        os.makedirs(os.path.join(get_base_dir(), 'data','h5_output'), exist_ok=True)
        tasks=[]
        if args.directory:
            for structure in glob.glob(args.directory+'/*.pdb'):
                tasks.append(Task(
                    process_structure,
                    (structure,
                    config,
                    'result',
                    )))
            processing_structure_and_store_h5=TaskLevel(tasks)
            tasks_aggr=[]
            
            os.makedirs(os.path.join(get_base_dir(), 'data','h5_output','directory_process'), exist_ok=True)
            
            tasks_aggr.append(Task(concat_hdf5_files,(
                        os.path.join(get_base_dir(), 'data','h5_output','directory_process',str(datetime.datetime.now()).replace('.',':').replace(' ','_')+'.h5'),
                        glob.glob(os.path.join(get_base_dir(), 'data','h5','result','*.h5')))))
            aggregate_h5=TaskLevel(tasks_aggr)
            run([processing_structure_and_store_h5,aggregate_h5])
            
        else:
            for structure in InputsConfig(config).TEST_FILES:
                tasks.append(Task(
                    process_structure,
                    (structure,
                    config,
                    'test',
                    df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target'],
                    )))
            for structure in InputsConfig(config).TRAIN_FILES:
                tasks.append(Task(
                    process_structure,
                    (structure,
                    config,
                    'train',
                    df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target'],
                    )))

            processing_structure_and_store_h5=TaskLevel(tasks)
            tasks_aggr=[]
            tasks_aggr.append(Task(concat_hdf5_files,(
                        os.path.join(get_base_dir(), 'data','h5_output','test.h5'),
                        glob.glob(os.path.join(get_base_dir(), 'data','h5','test','*.h5')))))
            tasks_aggr.append(Task(concat_hdf5_files,(
                        os.path.join(get_base_dir(), 'data','h5_output','train.h5'),
                        glob.glob(os.path.join(get_base_dir(), 'data','h5','train','*.h5')))))
            aggregate_h5=TaskLevel(tasks_aggr)
            run([processing_structure_and_store_h5,aggregate_h5])
        
    else:
        if config.data.production:
            if args.directory:
                for structure in glob.glob(args.directory+'/*.pdb'):
                    process_structure(structure,config,'test',None)
            elif args.pdb_file:
                process_structure(args.f,config,'test',None)
        
        else:
            df = read_target_csv(config.data)
            for structure in InputsConfig(config).TEST_FILES:
                process_structure(structure,config,'test',df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target'])
            for structure in InputsConfig(config).TRAIN_FILES:
                process_structure(structure,config,'train',df[df['description']==os.path.splitext(os.path.basename(structure))[0]]['target'])
            
            os.makedirs(os.path.join(get_base_dir(), 'data','h5_output'), exist_ok=True)
            concat_hdf5_files(
                    os.path.join(get_base_dir(), 'data','h5_output','test.h5'),
                    glob.glob(os.path.join(get_base_dir(), 'data','h5','test','*.h5')))
            concat_hdf5_files(
                    os.path.join(get_base_dir(), 'data','h5_output','train.h5'),
                    glob.glob(os.path.join(get_base_dir(), 'data','h5','train','*.h5')))
