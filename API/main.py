import os
from flask import Flask, abort, request, jsonify, json
from flask_cors import CORS

from scripts.generate_url import generate_task_id
from scripts.process_files import process_files
from config import DEBUG_MODE, STORAGE_DIR, STATUS_FILE


app = Flask(__name__)
CORS(app)


@app.route("/request_rmsd", methods=["GET", "POST"])
def execute_command():
    # generate unique task id
    task_id = generate_task_id()
    
    if len(request.files):
        # process files
        error = process_files(request.files, task_id)

        if not error:
            # return the task id
            return jsonify({
                "task_id": task_id,
            })
    
    return abort(400)   # bad request


@app.route("/check_rmsd/<url_path>", methods=["GET"])
def check_status(url_path: str):
    # try to find the status file of a request and send it back if it exists
    if url_path in os.listdir(STORAGE_DIR):
        dir_path = os.path.join(STORAGE_DIR, url_path)
        
        if STATUS_FILE in os.listdir(dir_path):
            return jsonify(json.load(open(os.path.join(dir_path, STATUS_FILE))))

    return abort(404)   # not found


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)
