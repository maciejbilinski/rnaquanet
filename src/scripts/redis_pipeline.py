import os
import sys
import time
from redis import Redis
from rq import Queue
from typing import Callable
from rq.job import Job


class Task:
    """
        Args:
            - function - [Callable] function
            - params - [tuple] containing parameters of 'function' in correct order
            - task_id - [str] short description; must be unique because it is used as a job_id within redis queue
    """
    def __init__(self, function: Callable, params: tuple=(), task_id: str=""):
        self.function = function
        self.task_id = task_id
        self.params = params

    """
        preparing task to run after defined in depends_on tasks list 
    """
    def return_with_dependance(self, _depends_on: list[Job]):
        if len(self.task_id)>0:
            return Queue.prepare_data(self.function, self.params, job_id=self.task_id, depends_on=_depends_on)
        else:
            return Queue.prepare_data(self.function, self.params, depends_on=_depends_on)
    
    
    """
        preparing task to run when it will be possible 
    """
    def return_without_dependance(self):
        if len(self.task_id)>0:
            return Queue.prepare_data(self.function, self.params, job_id=self.task_id)
        else:
            return Queue.prepare_data(self.function, self.params)


class TaskLevel:
    """
        Task stack. There are defines levels of processing. Eg. First layer runs tasks for filters cif files. Second layer extract features from cif files.
        Args:
            - tasks - list of Task objects
            - async_tasks - if False then the order of the tasks specified in TaskLevel
            is kept; if True then tasks are executed in random unpredictable order
    """
    def __init__(self, tasks: list[Task], async_tasks: bool = False):
        self._tasks = tasks
        self._wait = not async_tasks
    
    def wait(self): # next level need to wait for this level finish
        return self._wait
    
    def tasks(self):
        return self._tasks


def run(tasks_stack: list[TaskLevel]):
    redis = Redis('redis')
    q = Queue('feature_extraction', connection=redis)

    with q.connection.pipeline() as pipe:
        tasks_level_wait: list[Job] = []
        for task_level in tasks_stack:
            if len(tasks_level_wait) > 0:
                jobs = q.enqueue_many([task.return_with_dependance(tasks_level_wait[-1]) for task in task_level.tasks()])
            else:
                jobs = q.enqueue_many([task.return_without_dependance() for task in task_level.tasks()])
            if task_level.wait():
                tasks_level_wait.append(jobs)
                
        print("Tasks are prepared")
        pipe.execute() 
        print("Pipeline is running: check http://127.0.0.1:8080")

def test(lol):
        print(lol)
        time.sleep(2)
        print(lol+'2')


def check():
    t1=Task(test,('t1',))
    t2=Task(test,('t2',))
    tl1=TaskLevel([t1,t2])
    t3=Task(test,('t3',))
    t4=Task(test,('t4',))
    tl2=TaskLevel([t3,t4])
    run([tl1,tl2])
"""
EXAMPLE:
    def test(lol):
        print(lol)
    
    t1=Task(test,('sth, string',))
    t2=Task(test,('sth, string',))
    tl=TaskLevel([t1,t2])
    
    t3=Task(test,('sth, string',))
    t4=Task(test,('sth, string',))
    tl2=TaskLevel([t3,t4])

    run([tl,tl2])

    check process at http://127.0.0.1:8080
"""