from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql.json import JSONB

db = SQLAlchemy()


class PathwaysProgram(db.Model):
    pathways_program = db.Column(JSONB)
    updated_at = db.Column(db.TIMESTAMP)
    gs_row_identifier = db.Column(db.String, primary_key=True)

    def __init__(self, updated_at, pathways_program):
        self.gs_row_identifier = gs_row_identifier
        self.updated_at = updated_at
        self.pathways_program = pathways_program
