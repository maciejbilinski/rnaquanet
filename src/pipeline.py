from redis import Redis
from rq import Queue
from typing import List, Callable
import time
class Task:

    def __init__(self, function:Callable, params:tuple, description:str):
        self.function = function
        self.description = description
        self.params = params

    def return_with_dependance(self, depends_on):
        return Queue.prepare_data(self.function, self.params, job_id=self.description,depends_on=depends_on)
    
    def return_without_dependance(self):
        return Queue.prepare_data(self.function, self.params, job_id=self.description)

class TaskLevel:

    def __init__(self, tasks:List[Task], wait:bool=True):
        self.tasks=tasks
        self.wait=wait
    
    def get_wait(self): # next level need to wait for finish of this level
        return self.wait
    def get_tasks(self):
        return self.tasks



def run(tasks_stack:List[TaskLevel]):

    redis = Redis('redis',6379 )
    q = Queue('feature_extraction',connection=redis)

    with q.connection.pipeline() as pipe:
        tasks_level_wait=[]
        for task_level in tasks_stack:
            jobs = q.enqueue_many(
                [
                    task.return_with_dependance(tasks_level_wait[-1]) if len(tasks_level_wait)>0 else task.return_without_dependance() for task in task_level.get_tasks()
                ],
                pipeline=pipe
            )
            if task_level.get_wait():
                tasks_level_wait.append(jobs)
        print("Task are prepared")
        pipe.execute() 
        print("Pipeline is running: check http://server-address:8080")
