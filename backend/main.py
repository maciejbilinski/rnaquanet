from flask import Flask, abort, request, jsonify
from flask_cors import CORS
import random
import string
import os

app = Flask(__name__)
CORS(app)

# dictionary storing 
urls: dict[str, dict[str, any]] = {}

def generate_task_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=24))

@app.route("/get_rmsd", methods=["GET", "POST"])
def execute_command():
    data = request.json
    url_path = generate_task_id()

    # Store the task in the dictionary
    urls[url_path] = {
        "files": data["files"],
        "status": "PENDING"
    }

    # Construct the server command (modify this based on your needs)
    # command = f"your_server_command {' '.join(data['files'])}"

    # Execute the server command asynchronously (modify as needed)
    # os.system(command + " &")

    return jsonify({
        "url_path": url_path
    }), 200

@app.route("/check_rmsd/<url_path>", methods=["GET"])
def check_status(url_path: str):
    if url_path in urls:
        return jsonify({
            "status": urls[url_path]["status"]
        })
    else:
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True)