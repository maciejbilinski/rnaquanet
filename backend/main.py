import os
from flask import Flask, abort, request, jsonify, json
from flask_cors import CORS
from flasgger import Swagger
from flask_rq2 import RQ

from scripts.generate_task_id import generate_task_id
from scripts.process_files import process_files
from models.models import db, Task

# from a import eo
from config import APP_CONFIG, FILE_STORAGE_DIR, SWAGGER_TEMPLATE


app = Flask(__name__)
app.config.update(APP_CONFIG)

CORS(app)
Swagger(app, template=SWAGGER_TEMPLATE)  # Swagger UI is located at `api.url/apidocs/`
db.init_app(app)
rq = RQ(app)

queue = rq.get_queue()


@app.route("/request_rmsd", methods=["POST"])
def request_rmsd():
    """
    Request file processing and get the task ID.
    ---
    parameters:
      - name: files
        in: formData
        type: file
        required: true
        description: The files to process.
    responses:
      200:
        description: File processing has started and task ID was generated successfully.
        schema:
          properties:
            task_id:
              type: string

      400:
          description: Bad request.

    """
    # generate unique task id
    task_id = generate_task_id()

    if len(request.files):
        # process files
        error = process_files(queue, request.files, task_id)

        if not error:
            # return the task id
            return jsonify(
                {
                    "task_id": task_id,
                }
            )

    return abort(400)  # bad request


@app.route("/check_rmsd/<url_path>", methods=["GET"])
def check_rmsd(url_path: str):
    """
    Check the status of a task.
    ---
    parameters:
      - name: url_path
        in: path
        type: string
        required: true
        description: The URL path containing the task information.
    responses:
      200:
        description: Task status retrieved successfully.
        schema:
          properties:
            status:
              type: string
      404:
        description: Task not found.
    """
    # try to find requested resources and send it back if it exists
    # else return with 404
    task = db.get_or_404(Task, url_path)
    print(task.status)
    if url_path in os.listdir(FILE_STORAGE_DIR):
        dir_path = os.path.join(FILE_STORAGE_DIR, url_path)

        # if STATUS_FILE in os.listdir(dir_path):
        #     return jsonify(json.load(open(os.path.join(dir_path, STATUS_FILE))))

    return abort(404)  # not found


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
