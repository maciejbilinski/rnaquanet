
# =============================================
# main.py 
#
# Spec: 
# run processing pipeline preparing files for training and testing
# here are definied levels of concurrent processing:
# task = (function, description='task_description')
# task_level_1 = (TaskLevel(tasks=[Task(),Task()],nowait:bool=False))
# task_level_2 = (TaskLevel(tasks=[Task(),Task()],nowait:bool=False))
# run = [task_level_1,task_level_2]
# =============================================

from src import pipeline
def get_pipeline_tasks():
    return []





if __name__ == '__main__':
    pipeline.run(get_pipeline_tasks())

