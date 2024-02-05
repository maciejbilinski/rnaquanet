from typing import List
from sqlalchemy.orm import Mapped
from dataclasses import dataclass

from config import TASK_ID_LENGTH
from app import db


@dataclass
class File(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(256), nullable=False)
    status: str = db.Column(db.String(16), nullable=False)
    selectedModel: str = db.Column(db.String(16), nullable=False)
    selectedChain: str = db.Column(db.String(16), nullable=False)
    rmsd: float = db.Column(db.Float)
    task_id: str = db.Column(
        db.String(TASK_ID_LENGTH), db.ForeignKey("task.id"), nullable=False
    )


@dataclass
class Task(db.Model):
    id: str = db.Column(db.String(TASK_ID_LENGTH), primary_key=True)
    status: str = db.Column(db.String(16), nullable=False)
    timestamp: int = db.Column(db.Integer)
    files: Mapped[List[File]] = db.relationship("File", backref="task", lazy=True)
