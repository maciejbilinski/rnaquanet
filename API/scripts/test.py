import os
from random import randrange
from time import sleep

from scripts.save_as_json import save_as_json
from config import FILES_DIR, STORAGE_DIR, STATUS_FILE


def test(task_id):
    sleep(15)
    
    dir_path = os.path.join(STORAGE_DIR, task_id)
    file_names = os.listdir(os.path.join(dir_path, FILES_DIR))
    
    if (len(file_names)):
        save_as_json(
            {
                "status": "DONE",
                "results": { file_name: {"rmsd": randrange(0, 20), "error": 0} for file_name in file_names }
            },
            os.path.join(dir_path, STATUS_FILE)
        )
        return
        
    save_as_json(
        { "status": "ERROR" },
        os.path.join(dir_path, STATUS_FILE)
    )