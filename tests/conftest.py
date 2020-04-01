import json
import os

import pytest
from flask_migrate import upgrade

from google_pathways_api.app import create_app
from google_pathways_api.db.models import PathwaysProgram, db



@pytest.fixture
def app():
    os.environ['APP_ENV'] = 'TEST'
    app = create_app()

    return app 


@pytest.fixture
def pathways_programs(app):
    '''
    A fixture that adds two programs to the database.
    '''
    json_ld = {
        "@context": "http://schema.org/",
        "@type": "EducationalOccupationalProgram",
        "name": "Certified Nursing Assistant Program",
        "description": "This course helps participants cultivate the attitudes, skills and behaviors of a competent caregiver"
    }

    program_data = { 'updated_at': '2020-03-01', 'pathways_program': json.dumps(json_ld) }
    program_one = PathwaysProgram(**program_data)

    json_ld = {
        "@context": "http://schema.org/",
        "@type": "WorkBasedProgram",
        "name": "Customer Service and Sales Training",
        "description": "Provides training in Customer Service and Sales"
    }

    program_data = { 'updated_at': '2020-03-01', 'pathways_program': json.dumps(json_ld) }
    program_two = PathwaysProgram(**program_data)

    with app.app_context():
        db.session.add(program_one)
        db.session.add(program_two)
        db.session.commit()
