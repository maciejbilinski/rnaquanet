from random import randrange
from time import sleep

from models.models import db, Task
from app import app


def test(task_id):
    with app.app_context():
        sleep(1)

        print(f"???Started: {task_id}")
        task: Task | None = Task.query.get(task_id)
        task.status = "PENDING"
        db.session.commit()

        sleep(1)

        for file in task.files:
            file.rmsd = randrange(1, 20, 1)
            file.status = "SUCCESS"
        task.status = "DONE"
        db.session.commit()
        print(f"!!!Finished: {task_id}")
