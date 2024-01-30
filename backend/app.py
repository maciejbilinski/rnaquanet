from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_rq2 import RQ

from config import APP_CONFIG


app = Flask(__name__)
app.config.update(APP_CONFIG)

db = SQLAlchemy()
db.init_app(app)

rq = RQ(app)
queue = rq.get_queue()
