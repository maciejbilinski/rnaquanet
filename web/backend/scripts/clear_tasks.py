import shutil, os
from time import time

from app import app, db
from models.models import Task
from config import FILE_STORAGE_DIR, DB_CLEAR_INTERVAL


def clear_task(task_id: str):
    with app.app_context():
        Task.query.filter(Task.id == task_id).delete()
        db.session.commit()
        shutil.rmtree(os.path.join(FILE_STORAGE_DIR, task_id))


def clear_old_tasks():
    with app.app_context():
        old_tasks_q = Task.query.filter(
            Task.timestamp + DB_CLEAR_INTERVAL.total_seconds() < time()
        )
        old_tasks: list[Task] = old_tasks_q.all()
        for t in old_tasks:
            dir_path = os.path.join(FILE_STORAGE_DIR, t.id)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
        old_tasks_q.delete()
        db.session.commit()
