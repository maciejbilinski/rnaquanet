from redis import Redis
from rq import Queue
from typing import Callable
from rq.job import Job


class Task:
    def __init__(self, function: Callable, params: tuple, description: str):
        self.function = function
        self.description = description
        self.params = params

    def return_with_dependance(self, depends_on: Job):
        return Queue.prepare_data(self.function, self.params, job_id=self.description, depends_on=depends_on)
    
    def return_without_dependance(self):
        return Queue.prepare_data(self.function, self.params, job_id=self.description)


class TaskLevel:
    def __init__(self, tasks: list[Task], wait: bool = True):
        self.tasks = tasks
        self.wait = wait
    
    def get_wait(self): # next level need to wait for finish of this level
        return self.wait
    
    def get_tasks(self):
        return self.tasks


def run(tasks_stack: list[TaskLevel]):
    # TODO: currently the queue does not work correctly. the server often
    # crashes when trying to view 'started jobs'. most often TypeError
    # of some kind so possibly there's something wrong with how the queue is
    # built from the jobs
    redis = Redis('redis')
    q = Queue('feature_extraction', connection=redis)

    with q.connection.pipeline() as pipe:
        tasks_level_wait: list[Job] = []
        for task_level in tasks_stack:
            jobs = q.enqueue_many([task.return_with_dependance(tasks_level_wait[-1])
                                   if (len(tasks_level_wait) > 0)
                                   else task.return_without_dependance()
                                   for task in task_level.get_tasks()
                ],
                pipeline=pipe
            )
            if task_level.get_wait():
                tasks_level_wait.append(jobs)
                
        print("Tasks are prepared")
        pipe.execute() 
        print("Pipeline is running: check http://127.0.0.1:8080")
