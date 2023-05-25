import glob
import os
import shutil
from tqdm import tqdm

def prepare_catalogs(src_dir: str, dest_dir: str, mappings: list[dict]) -> str:
    """
    Prepares the catalogs.

    Args:
        src_dir: source directory
        dest_dir: destination directory
        mappings: a list of dictionaries containing 'src' and 'dest' keys
        specifying the files/directories to move
    Returns:
        destination directory path
    """
    for mapping in mappings:
        src = f'{src_dir}/{mapping["src"]}'
        dest = f'{dest_dir}/{mapping["dest"]}'
        shutil.move(src, dest)
    
    return dest_dir


def filter_files(src: str, dest: str) -> bool:
    """
    Reads and filters each PDB file in the 'train' and 'test' subfolders
    within src and writes them respectively into dest.
    Additionally moves 'scores.sc' from src to dest.

    Args:
        src: source directory
        dest: destination directory
    Returns:
        None 
    """
    # Find all PDB files within directory and subdirectories
    pattern = f'{src}/**/*.pdb'
    src_files = glob.glob(pattern, recursive=True)

    # Progress bar
    total_files = len(src_files)+1
    progress_bar = tqdm(total=total_files, unit='f')

    for in_filename in src_files:
        name, ext = os.path.splitext(in_filename)
        out_filename = f'{name}_filtered{ext}'.replace(src, dest)
        out_dir = os.path.dirname(out_filename)
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with open(in_filename, 'r') as input_file:
            with open(out_filename, 'w') as output_file:
                for line in input_file:
                    if line.startswith('ATOM') or line.startswith('TER'):
                        output_file.write(line)
        
        progress_bar.update()
    
    shutil.move(f'{src}/scores.sc', f'{dest}/scores.sc')
    progress_bar.update()
    progress_bar.close()
    return True
