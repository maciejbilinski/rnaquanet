from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class A(db.model):
    