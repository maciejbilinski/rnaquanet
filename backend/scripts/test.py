import os
from random import randrange
from time import sleep

from config import FILE_STORAGE_DIR
from scripts.save_as_json import save_as_json


def test(task_id):
    print(f"???Started: {task_id}")
    sleep(15)

    file_names = os.listdir(os.path.join(FILE_STORAGE_DIR, task_id))

    if len(file_names):
        # save_as_json(
        #     {
        #         "status": "DONE",
        #         "results": {
        #             file_name: {"rmsd": randrange(0, 20), "error": 0}
        #             for file_name in file_names
        #         },
        #     },
        #     os.path.join(dir_path, STATUS_FILE),
        # )
        print(f"!!!Finished: {task_id}")
        return

    # save_as_json({"status": "ERROR"}, os.path.join(dir_path, STATUS_FILE))
