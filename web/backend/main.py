from flask import jsonify, abort, request
from flask_cors import CORS
from flasgger import Swagger
import json

from scripts.generate_task_id import generate_task_id
from scripts.process_files import process_files
from models.models import Task

from config import SWAGGER_TEMPLATE, AVAILABLE_MODELS
from app import app, db
from scripts.form_file_handler import retrieve_models_and_chains
from scripts.clear_tasks import clear_old_tasks

CORS(app)
Swagger(app, template=SWAGGER_TEMPLATE)  # Swagger UI is located at `api.url/apidocs/`


@app.route("/get_models_and_chains", methods=["POST", "GET"])
def get_models_and_chains():
    """
    Request an analysis and return of files' models and chains.
    ---
    parameters:
      - name: files
        in: formData
        type: file
        required: true
        description: The files to analyze.
    responses:
      200:
        description: Files analyzed successfully.
        type: object

      404:
        description: No chains/models found.
    """
    return jsonify(
        {
            file.filename: retrieve_models_and_chains(file)
            for file in request.files.values()
        }
    )


# @app.route("/request_rmsd/<task_id>", methods=["POST"])
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
      - name: form
        in: json string
        required: true
        content:
          application/json:
            schema:
              type: object
        description: Object containing files and their chosen models & chains.
    responses:
      200:
        schema:
          properties:
            task_id:
              type: string
        description: File processing has started and task ID was generated successfully.

      400:
          description: Bad request.

    """
    # generate unique task id
    task_id = generate_task_id()
    data = json.loads(request.form.get("data"))
    model_name = request.form.get("modelName")

    if len(request.files) and model_name in AVAILABLE_MODELS:
        # process files
        error = process_files(request.files, data, model_name, task_id)

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
                  status:
                    type: string
                  selectedModel:
                    type: string
                  selectedChain:
                    type: string
                  rmsd:
                    type: number
                  task_id:
                    type: string

      404:
        description: Task not found.
    """
    # try to find requested resources and send it back if it exists
    # else return 404
    task: Task = Task.query.get_or_404(task_id)

    return {
        "status": task.status,
        "files": [jsonify(file).json for file in task.files],
    }


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        clear_old_tasks()
        app.run(host="0.0.0.0", port=5000)
