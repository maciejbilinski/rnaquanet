import os
from dataclasses import dataclass


def change_dir(directory: str) -> None:
    """
    Change dir relative to file

    Args:
        directory: dir relative to file; should specify the root dir of the
        project (where data directory is present)
    """
    relative_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))
    os.chdir(relative_dir)


# parameters
@dataclass
class data_downloading:
    ares_dataset_url: str = 'https://dl.dropboxusercontent.com/s/r4hgjs4xgmkmaxj/classics_train_val.tar?dl=0'
    ares_archive_path: str = 'data/00_temp'
    ares_dataset_path: str = 'data/01_raw'


@dataclass
class feature_extraction:
    structure_descriptor_params = {
        'atom_for_distance_calculations': "C1'",
        'max_euclidean_distance': 16.0
    }
    score_file_path: str = 'data/01_raw/scores.sc' #FIXME:jeżeli się da pobrać ten parametr z preprocessing_data.yml to usuncie to
    path = {
        'src': 'data/03_filtered',
        'dest': 'data/04_primary'
    }
        

@dataclass
class prepare_docker:
    structure_descriptor_docker_image: str = 'https://rnasolo.cs.put.poznan.pl/media/describe_structure.tar.xz'
    docker_image_path: str = "data/00_temp"
    raise_on_error: bool = True


@dataclass
class preprocessing_data:
    # Maps which files/directories to move and where
    prepare_catalogs_src: str = 'data/01_raw'
    prepare_catalogs_dest: str = 'data/02_intermediate'
    mappings = [
        {
            'src': 'example_train',
            'dest': 'train'
        },
        {
            'src': 'example_val',
            'dest': 'test'
        },
        {
            'src': 'scores.sc',
            'dest': 'scores.sc'
        }
    ]
    filter_files_dest: str = 'data/03_filtered'
