import os, shutil
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from rq import Queue

from config import TEMP_FILE_STORAGE_DIR
from scripts.test import test
from models.models import db, Task, File
from scripts.form_file_handler import extract_chain


def process_files(
    queue: Queue,
    files: ImmutableMultiDict[str, FileStorage],
    data: dict[str, dict[str, str]],
    task_id: str,
):
    # create directories:
    # - `{TEMP_FILE_STORAGE_DIR}` if it does not exist yet
    # - `{task_id}` directory containing files from current task
    temp_dir_path = os.path.join(TEMP_FILE_STORAGE_DIR, task_id)
    os.makedirs(temp_dir_path, exist_ok=True)
    try:
        db_task = Task(id=task_id, status="QUEUED")
        db.session.add(db_task)

        # save each file
        for file in files.values():
            file_name = secure_filename(file.filename)
            temp_file_path = os.path.join(temp_dir_path, file_name)
            file.save(temp_file_path)

            # extract selected chain from the file and save it
            error = extract_chain(
                task_id,
                file_name,
                data[file.filename]["selectedModel"],
                [data[file.filename]["selectedChain"]],
            )
            # add file info to the db
            db.session.add(
                File(
                    name=file_name,
                    status=("ERROR" if error else "WAITING"),
                    selectedModel=data[file.filename]["selectedModel"],
                    selectedChain=data[file.filename]["selectedChain"],
                    task=db_task,
                )
            )

        job = queue.enqueue(test, task_id)

    except Exception as e:
        db_task: Task | None = Task.query.get(task_id)
        db_task.status = "ERROR"

        print(e)
        return 1
    finally:
        db.session.commit()
        shutil.rmtree(temp_dir_path)

    return 0
