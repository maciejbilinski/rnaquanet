from flask import Flask, abort, request, jsonify
from flask_cors import CORS

from scripts.generate_url import generate_task_id
from scripts.process_files import process_files


app = Flask(__name__)
CORS(app)

# dictionary storing 
tasks: dict[str, dict[str, any]] = {}


@app.route("/get_rmsd", methods=["GET", "POST"])
def execute_command():
    files = request.files
    print(request.files)
    print(files.getlist("file_0"))
    task_id = generate_task_id()

    # store the generated url
    tasks[task_id] = {
        "files": files,
        "status": "PENDING"
    }

    # process files
    process_files(files)

    # return url
    return jsonify({
        "task_id": task_id
    })


@app.route("/check_rmsd/<url_path>", methods=["GET"])
def check_status(url_path: str):
    if url_path in tasks:
        return jsonify({
            "status": tasks[url_path]["status"]
        })
    else:
        return abort(404)


if __name__ == "__main__":
    app.run(debug=True)