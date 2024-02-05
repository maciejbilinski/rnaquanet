import shutil, os

from app import app, db
from models.models import Task
from config import FILE_STORAGE_DIR


def clear_task(task_id: str):
    with app.app_context():
        Task.query.filter(Task.id == task_id).delete()
        db.session.commit()
        shutil.rmtree(os.path.join(FILE_STORAGE_DIR, task_id))
