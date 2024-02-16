import os
from models.models import Task, Descriptor
from rnaquanet.network.rnaquanet import get_rmsd, get_local_rmsd
from app import app, db, queue
from web.backend.scripts.clear_tasks import clear_task
from config import FILE_STORAGE_DIR, DB_CLEAR_INTERVAL


def task_handler(analysis_type: str, task_id: str):
    with app.app_context():
        db_task: Task | None = Task.query.get(task_id)
        db_task.status = "PENDING"
        db.session.commit()

        dir_path = os.path.join(FILE_STORAGE_DIR, task_id)
        for db_file in db_task.files:
            try:
                if analysis_type == "global":
                    rmsd = abs(get_rmsd("ares", os.path.join(dir_path, db_file.name)))
                    if rmsd:
                        db_file.rmsd = rmsd
                        db_file.status = "SUCCESS"
                    else:
                        raise
                elif analysis_type == "local":
                    output = get_local_rmsd(os.path.join(dir_path, db_file.name))
                    if not output.empty and not output["predicted_rmsd"].empty:
                        for _, desc in output.iterrows():
                            desc["predicted_rmsd"] = abs(desc["predicted_rmsd"])
                            db.session.add(
                                Descriptor(
                                    name=desc["descriptor_name"],
                                    rmsd=desc["predicted_rmsd"],
                                    sequence=desc["sequence"],
                                    residue_range=desc["residue_range"],
                                    file=db_file,
                                )
                            )

                        db_file.rmsd = sum(output["predicted_rmsd"]) / len(output["predicted_rmsd"])
                        db_file.status = "SUCCESS"
                    else:
                        raise

            except Exception as e:
                print(e)
                db_file.status = "ERROR"

        db_task.status = "DONE"
        db.session.commit()

        queue.enqueue_in(DB_CLEAR_INTERVAL, clear_task, task_id)
