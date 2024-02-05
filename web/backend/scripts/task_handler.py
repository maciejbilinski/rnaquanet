import os

from models.models import Task
from rnaquanet.network.rnaquanet import get_rmsd
from app import app, db, queue
from web.backend.scripts.clear_tasks import clear_task
from config import FILE_STORAGE_DIR, DB_CLEAR_INTERVAL


def task_handler(model_name: str, task_id: str):
    with app.app_context():
        db_task: Task | None = Task.query.get(task_id)
        db_task.status = "PENDING"
        db.session.commit()

        dir_path = os.path.join(FILE_STORAGE_DIR, task_id)
        for file in db_task.files:
            try:
                rmsd = abs(get_rmsd(model_name, os.path.join(dir_path, file.name)))
                if rmsd:
                    file.rmsd = rmsd
                    file.status = "SUCCESS"
                else:
                    raise

            except Exception as e:
                print(e)
                file.status = "ERROR"

        db_task.status = "DONE"
        db.session.commit()

        queue.enqueue_in(DB_CLEAR_INTERVAL, clear_task, task_id)
