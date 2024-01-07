from flask_sqlalchemy import SQLAlchemy

from config import TASK_ID_LENGTH

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.String(TASK_ID_LENGTH), primary_key=True)
    status = db.Column(db.String(16), nullable=False)
    files = db.relationship("File", backref="task", lazy=True)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    is_temp = db.Column(db.Boolean, nullable=False, default=False)
    task_id = db.Column(
        db.String(TASK_ID_LENGTH), db.ForeignKey("task.id"), nullable=False
    )
