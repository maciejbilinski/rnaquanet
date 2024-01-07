from random import randrange
from time import sleep
from models.models import db, Task


def test(task_id):
    sleep(2)

    print(f"???Started: {task_id}")
    task: Task | None = Task.query.get(task_id)
    for file in task.files:
        file.status = "PENDING"
    db.session.commit()

    sleep(2)

    for file in task.files:
        file.rmsd = randrange(1, 20, 1)
        file.status = "DONE"
    db.session.commit()
    print(f"!!!Finished: {task_id}")
