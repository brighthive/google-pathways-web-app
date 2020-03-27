from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql.json import JSONB

db = SQLAlchemy()


class PathwaysProgram(db.Model):
    id = db.Column(db.String, primary_key=True)
    pathways_program = db.Column(JSONB)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self):
        self.id = str(uuid4())
