import os
import shutil


def clear_catalog(path):
    for root, dirs, files in os.walk(os.path.join(path,'*')): 
        for f in files:
            if f != '.gitkeep':
                os.remove(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
