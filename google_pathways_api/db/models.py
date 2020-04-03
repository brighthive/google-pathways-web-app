from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql.json import JSONB

db = SQLAlchemy()


class PathwaysProgram(db.Model):
    id = db.Column(db.String, primary_key=True)
    pathways_program = db.Column(JSONB)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, updated_at, pathways_program, id=None):
        self.updated_at = updated_at
        self.pathways_program = pathways_program
        self.id = id or str(uuid4())
