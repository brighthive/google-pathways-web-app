import json

from google_pathways_web_app.db.models import PathwaysProgram

json_ld = {
    "@context": "http://schema.org/",
    "@type": "WorkBasedProgram",
    "name": "Customer Service and Sales Training",
    "description": "Provides training in Customer Service and Sales",
}


def test_pathways_programs_default_id(client):
    program = PathwaysProgram(
        updated_at="2020-02-01 1:31:10", pathways_program=json.dumps(json_ld)
    )

    assert program.id != None


def test_pathways_programs_json(client):
    """Assert that the `pathways_program` stores JSON, which can be decoded
    using the Python `json` module."""
    program = PathwaysProgram(
        updated_at="2020-02-01 1:31:10", pathways_program=json.dumps(json_ld)
    )

    json_loads = json.loads(program.pathways_program)

    assert type(json_loads) == dict
