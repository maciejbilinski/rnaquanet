import os, requests
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from rq import Queue

from config import FILE_STORAGE_DIR, TEMP_FILE_STORAGE_DIR
from scripts.test import test
from models.models import db, Task, File
from scripts.form_file_handler import retrieve_models_and_chains, process


def process_files(
    queue: Queue, files: ImmutableMultiDict[str, FileStorage], task_id: str
):
    try:
        # create directories:
        # - `{TEMP_FILE_STORAGE_DIR}` if it does not exist yet
        # - `{task_id}` directory containing files from current task
        dir_path = os.path.join(TEMP_FILE_STORAGE_DIR, task_id)
        os.makedirs(dir_path, exist_ok=True)

        db_task = Task(id=task_id, status="QUEUED")
        db.session.add(db_task)
        
        # save each file
        for file in files.values():
            # file from protein data bank, download it
            if file.name.endswith("_pdb"):
                file_name = f"{file.filename}.pdb"
                url = f"http://files.rcsb.org/download/{file_name}.pdb"
                res = requests.get(url, allow_redirects=True)

                if res.status_code == 200:
                    temp_file_path = os.path.join(dir_path, file_name)
                    with open(temp_file_path, "wb+") as bin_file_handle:
                        bin_file_handle.write(res.content)
                else:
                    # TODO error while processing file (file does not exists in protein data bank)
                    return 1
            else:
                file_name = secure_filename(file.filename)
                temp_file_path = os.path.join(dir_path, file_name)
                file.save(temp_file_path)

            # models = get_models_with_chains(task_id, file_name)
            # print(models)
            # if not models:
            #     return 1

            p = process(task_id, file_name, "xdd", 0, [0, 9])
            # print(p)
            db.session.add(File(status="WAITING", name=file_name, task=db_task))

        db.session.commit()

        # TODO remove the dummy output queue and instead execute a command to process saved files
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
        job = queue.enqueue(test, task_id)

    except Exception as e:
        print(e)
        return 1
    return 0
