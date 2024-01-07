from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from flask_rq2 import RQ
from flasgger import Swagger

from scripts.generate_task_id import generate_task_id
from scripts.process_files import process_files
from models.models import db, Task

from config import APP_CONFIG, SWAGGER_TEMPLATE


def init_app():
    app = Flask(__name__)
    app.config.update(APP_CONFIG)
