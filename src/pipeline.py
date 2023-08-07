import time
from redis import Redis
from rq import Queue
from typing import Callable
from rq.job import Job

# TODO: please check if docstrings are correct, they might be wrong
class Task:
    """
    Args:
    - function - function Callable
    - params - tuple containing parameters of 'function' in correct order
    - description - short description; must be unique because it is used as a
    job_id within redis queue
    """
    def __init__(self, function: Callable, params: tuple, description: str):
        self.function = function
        self.description = description
        self.params = params

    def return_with_dependance(self, depends_on: Job):
        return Queue.prepare_data(self.function, self.params, job_id=self.description, depends_on=depends_on)
    
    def return_without_dependance(self):
        return Queue.prepare_data(self.function, self.params, job_id=self.description)


class TaskLevel:
    """
    Args:
    - tasks - list of Task objects
    - async_tasks - if False then the order of the tasks specified in TaskLevel
    is kept; if True then tasks are executed in random unpredictable order
    """
    def __init__(self, tasks: list[Task], async_tasks: bool = False):
        self._tasks = tasks
        self._wait = not async_tasks
    
    def wait(self): # next level need to wait for finish of this level
        return self._wait
    
    def tasks(self):
        return self._tasks


def run(tasks_stack: list[TaskLevel]):
    # TODO: currently the queue does not work correctly. the timestamp could
    # not be formatted in the specified format. also 'NoneType' object has no
    # attribute 'id'. so possibly there's something wrong with how the queue is
    # built from the jobs
    redis = Redis('redis')
    q = Queue('feature_extraction', connection=redis)

    with q.connection.pipeline() as pipe:
        tasks_level_wait: list[Job] = []
        for task_level in tasks_stack:
            jobs = q.enqueue_many([task.return_with_dependance(tasks_level_wait[-1])
                                   if (len(tasks_level_wait) > 0)
                                   else task.return_without_dependance()
                                   for task in task_level.tasks()
                ],
                pipeline=pipe
            )
            if task_level.wait():
                tasks_level_wait.append(jobs)
                
        print("Tasks are prepared")
        pipe.execute() 
        print("Pipeline is running: check http://127.0.0.1:8080")
