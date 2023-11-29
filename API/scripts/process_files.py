import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from threading import Thread

from scripts.save_as_json import save_as_json
from config import FILES_DIR, STORAGE_DIR, STATUS_FILE
from scripts.test import test


def process_files(files: ImmutableMultiDict[str, FileStorage], task_id: str):
    try:
        # create directories:
        # - `{STORAGE_DIR}` if it does not exist yet
        # - `{task_id}` directory exclusive and identifying current task
        # - `files` where all files will be stored
        dir_path = os.path.join(STORAGE_DIR, task_id)
        files_dir_path = os.path.join(dir_path, FILES_DIR)
        os.makedirs(files_dir_path, exist_ok=True)
        
        save_as_json(
            { "status": "PENDING" },
            os.path.join(dir_path, STATUS_FILE)
        )
        
        # save each file
        for file in files.values():
            filepath = os.path.join(files_dir_path, secure_filename(file.filename))
            file.save(filepath)
        
        print("almost testing")
        # TODO process saved files in a seperate process/thread
        Thread(target=test, args=[task_id]).start()  # TODO remove, it's temp for testing
        
    except Exception:
        return 1
    return 0
