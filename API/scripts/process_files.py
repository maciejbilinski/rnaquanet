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
        
        # TODO remove the dummy output thread and instead execute a command to process saved files
        # after files are processed, write to their corresponding `status.json` file in this format:
        # {
        #     "status": "DONE",         # or "ERROR" if there was a general error and no files have been processed
        #     "results": {
        #         "file_name_0": {
        #             "rmsd": {rmsd},
        #             "error": 0        # or 1 if this file could not be processed due to an error (we can add more error types if needed)
        #         },
        #         "file_name_1": {
        #             ...
        #         },
        #         ...
        #     }
        # }
        # (if we use Python to write to `status.json`, we can just use `save_as_json.py` function from `API/scripts`)
        # remember to delete `files/` directory after files are processed to save space
        Thread(target=test, args=[task_id]).start()
        
    except Exception:
        return 1
    return 0
