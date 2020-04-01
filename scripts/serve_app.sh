#!/bin/sh
WORKERS=4

bash scripts/migrate.sh && \
gunicorn --workers=$WORKERS -b 0.0.0.0:8000 wsgi:app --reload --worker-class gevent --timeout 600