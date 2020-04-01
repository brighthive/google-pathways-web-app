import pytest

from google_pathways_api.db.models import PathwaysProgram, db


def test_pathways_ep(client, pathways_programs):
    resp = client.get('/pathways')

    assert resp.status_code == 200
    
    db.session.query(PathwaysProgram).delete()
    db.session.commit()


def test_pathways_script(client, pathways_programs):
    resp = client.get('/pathways')
    clean_resp = resp.data.decode("utf-8").replace("\\", "").replace("\n", "")
    clean_resp_no_space = ' '.join(clean_resp.split())
    script_tag = '<script type="application/ld+json"> "{"@context": "http://schema.org/", "@type": "EducationalOccupationalProgram", "name": "Certified Nursing Assistant Program", "description": "This course helps participants cultivate the attitudes, skills and behaviors of a competent caregiver"}" </script>'

    assert script_tag in clean_resp_no_space 

    db.session.query(PathwaysProgram).delete()
    db.session.commit()


def test_pathways_links(client, pathways_programs):
    resp = client.get('/pathways')
    links = '"links": [{"rel": "next", "href": "/pathways?page=2"}, {"rel": "prev", "href": ""}]'

    assert links in resp.data.decode("utf-8")

    db.session.query(PathwaysProgram).delete()
    db.session.commit()


@pytest.mark.parametrize('page,program_type', [
    ('1', 'EducationalOccupationalProgram'),
    ('2', 'WorkBasedProgram'),
])
def test_pathways_pagination(client, pathways_programs, page, program_type):
    resp = client.get(f'/pathways?page={page}')

    assert program_type in resp.data.decode("utf-8")

    db.session.query(PathwaysProgram).delete()
    db.session.commit()