import random, string, os

from config import STORAGE_DIR, TASK_ID_LENGTH


# generate a unique task ID
def generate_task_id():
    while True:
        task_id = "".join(random.choices(string.ascii_letters + string.digits, k=TASK_ID_LENGTH))
        
        # if {STORAGE_DIR} does not exist or task with the same name does not exist yet, accept this task_id
        if not os.path.isdir(STORAGE_DIR) or task_id not in os.listdir(STORAGE_DIR):
            return task_id