FROM python:3.7

WORKDIR /google-pathways-web-app

ADD google_pathways_web_app google_pathways_web_app
ADD data data
ADD migrations migrations
ADD wsgi.py wsgi.py

ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install pipenv && pipenv install --system && pipenv install --dev --system

ADD scripts scripts
RUN chmod +x scripts/serve_app.sh
RUN chmod +x scripts/migrate.sh

ENTRYPOINT [ "/google-pathways-web-app/scripts/serve_app.sh" ]
