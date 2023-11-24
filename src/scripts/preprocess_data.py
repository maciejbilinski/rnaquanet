import argparse
from multiprocessing import Pool
import sys
import os
import glob
import multiprocessing as mp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from tqdm import tqdm
from rnaquanet import get_base_dir
from src.data.preprocessing.hdf5_utils import concat_hdf5_files
from src.config.os import change_dir
from src.config.config import RnaquanetConfig
from src.config.prepare_target_set import read_target_csv
from src.data.preprocessing.preprocess_utils import (
    process_structure,
    process_structure_f,
)
from src.config.inputs import InputsConfig


parser = argparse.ArgumentParser(
    usage="%(prog)s",
    prog="RNAquanet",
    description="Run input processing",
)
parser.add_argument(
    "-d", "--directory", help="Structure source directory [absolute path]"
)

parser.add_argument(
    "-f", "--pdb-file", help="PDB file to preprocess"
)
parser.add_argument(
    "-o", "--output-directory", help="Output preprocessing directory [absolute path]"
)
"""
Preprocess pdf files from given directory.

Args:
- config - rnaquanet YML config file
- directory - pdb source directory

Returns:
- None

"""
def process_directory(config:RnaquanetConfig, source_directory:str,output_directory:str):
    for structure in glob.glob(source_directory + "/*.pdb"):
        process_structure(structure, config, "test", None)

    os.makedirs(
        os.path.join(output_directory),
        exist_ok=True,
    )
    concat_hdf5_files(
        os.path.join(output_directory, config.data.download.name + ".h5"),
        glob.glob(
            os.path.join(
                get_base_dir(), "data", "h5", config.data.download.name, "*.h5"
            )
        ),
    )


if __name__ == "__main__":
    change_dir("../..")
    config = RnaquanetConfig("config.yml")
    args = parser.parse_args()



    if config.data.production:
        if args.output_directory is None:
            raise Exception('output_directory is not definied')
        if args.directory:
            process_directory(config, args.directory, args.output_directory)
        elif args.pdb_file:
            process_structure(args.pdb_file, config, args.output_directory, None)

    if not config.data.production:
        df = read_target_csv(config.data)
        # parallel processing test structures
        with Pool(mp.cpu_count()) as pool:
            for _ in tqdm(
                enumerate(
                    pool.imap_unordered(
                        process_structure_f,
                        [
                            [
                                structure,
                                config,
                                os.path.join(get_base_dir(), 'data','h5',config.data.download.name,'test'),
                                df[
                                    df["description"]
                                    == os.path.splitext(os.path.basename(structure))[0]
                                ]["target"],
                            ]
                            for structure in InputsConfig(config).TEST_FILES
                        ],
                    )
                ),
                total=len(InputsConfig(config).TEST_FILES),
                unit="f",
            ):
                continue
        # parallel processing train structures

        with Pool(mp.cpu_count()) as pool:
            for _ in tqdm(
                enumerate(
                    pool.imap_unordered(
                        process_structure_f,
                        [
                            [
                                structure,
                                config,
                                os.path.join(get_base_dir(), 'data','h5',config.data.download.name,'train'),
                                df[
                                    df["description"]
                                    == os.path.splitext(os.path.basename(structure))[0]
                                ]["target"],
                            ]
                            for structure in InputsConfig(config).TRAIN_FILES
                        ],
                    )
                ),
                total=len(InputsConfig(config).TRAIN_FILES),
                unit="f",
            ):
                continue
        
        # concating train and test dataset into single h5 file
        os.makedirs(
            config.data.processing_output.h5_output,
            exist_ok=True,
        )
        concat_hdf5_files(
            os.path.join(config.data.processing_output.h5_output, "test.h5"),
            glob.glob(
                os.path.join(
                    get_base_dir(),
                    "data",
                    "h5",
                    config.data.download.name,
                    "test",
                    "*.h5",
                )
            ),
        )
        concat_hdf5_files(
            os.path.join(config.data.processing_output.h5_output, "train.h5"),
            glob.glob(
                os.path.join(
                    get_base_dir(),
                    "data",
                    "h5",
                    config.data.download.name,
                    "train",
                    "*.h5",
                )
            ),
        )
