from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from flask_rq2 import RQ
from flasgger import Swagger

from scripts.generate_task_id import generate_task_id
from scripts.process_files import process_files
from models.models import db, Task

# from a import eo
from config import APP_CONFIG, SWAGGER_TEMPLATE


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
            return jsonify({"task_id": task_id})

    return abort(400)  # bad request


@app.route("/check_rmsd/<task_id>", methods=["GET"])
def check_rmsd(task_id: str):
    """
    Check the status of a task.
    ---
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
        description: The URL path containing the task ID.
    responses:
      200:
        description: Task data retrieved successfully.
        schema:
          properties:
            status:
              type: string
            files:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  is_temp:
                    type: boolean
                  status:
                    type: string
                  rmsd:
                    type: number
                  task_id:
                    type: string
                  
      404:
        description: Task not found.
    """
    # try to find requested resources and send it back if it exists
    # else return with 404
    task: Task = Task.query.get_or_404(task_id)

    return {
        "status": task.status,
        "files": [jsonify(file).json for file in task.files],
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run()
