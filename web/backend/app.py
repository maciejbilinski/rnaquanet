from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_rq2 import RQ
from rq import Queue
import logging, warnings

from config import APP_CONFIG


app = Flask(__name__, static_url_path='', 
            static_folder='/app/web/frontend/dist',
            template_folder='/app/web/frontend/dist'
            )
app.config.update(APP_CONFIG)
log = logging.getLogger("werkzeug")
log.disabled = not APP_CONFIG["DEBUG"]
if not APP_CONFIG["DEBUG"]:
    warnings.filterwarnings("ignore")

db = SQLAlchemy()
db.init_app(app)

rq = RQ(app, default_timeout=-1)
queue: Queue = rq.get_queue()
