import os

from models.models import db, Task
from rnaquanet.network.rnaquanet import get_rmsd
from app import app
from config import FILE_STORAGE_DIR


def test(task_id):
    with app.app_context():
        print(f"TASK Started: {task_id}")
        task: Task | None = Task.query.get(task_id)
        task.status = "PENDING"
        db.session.commit()

        dir_path = os.path.join(FILE_STORAGE_DIR, task_id)
        for file in task.files:
            try:
                rmsd = get_rmsd("ares", os.path.join(dir_path, file.name))
                if rmsd:
                    file.rmsd = rmsd
                    file.status = "SUCCESS"
                else:
                    raise

            except Exception as e:
                print(e)
                file.status = "ERROR"
        
        task.status = "DONE"
        db.session.commit()
        print(f"TASK Finished: {task_id}")
