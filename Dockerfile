FROM python:3.7

WORKDIR /google-pathways-api

ADD google_pathways_api google_pathways_api
ADD migrations migrations
ADD tests tests
ADD wsgi.py wsgi.py
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install pipenv && pipenv install --system && pipenv install --dev --system

ADD scripts scripts 
RUN chmod +x scripts/serve_app.sh
RUN chmod +x scripts/migrate.sh