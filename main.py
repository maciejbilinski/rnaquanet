
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
from src.pipeline import Task, TaskLevel, run
from scripts import data_downloading as t1, preprocessing_data as t2

def get_pipeline_tasks():
    data_downloading = TaskLevel([
        Task(t1.download_ares_archive,
             params=(t1.params.ares_dataset_url, t1.params.ares_archive_path),
             description='download_ares_archive'),
        Task(t1.extract_ares_archive,
             params=(t1.params.ares_archive_path, t1.params.ares_dataset_path),
             description='extract_ares_archive')
    ], wait=False)

    preprocessing_data = TaskLevel([
        Task(t2.prepare_catalogs,
             params=(t2.params.prepare_catalogs_src, t2.params.prepare_catalogs_dest, t2.params.mappings),
             description='prepare_catalogs'),
        Task(t2.filter_files,
             params=(t2.params.prepare_catalogs_dest, t2.params.filter_files_dest),
             description='filter_files')
    ], wait=True)

    pipeline = [
        data_downloading,
        preprocessing_data
    ]

    return pipeline


if __name__ == '__main__':
    run(get_pipeline_tasks())
