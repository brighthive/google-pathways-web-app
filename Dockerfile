FROM python:3.7

WORKDIR /google-pathways-api

ADD google_pathways_api google_pathways_api
ADD migrations migrations
ADD wsgi.py wsgi.py
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install pipenv && pipenv install --system && pipenv install --dev --system

ADD cmd.sh cmd.sh
RUN chmod +x cmd.sh


ADD tests tests
RUN chmod +x tests/run_tests.sh

ADD wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh