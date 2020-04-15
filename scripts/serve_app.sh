#!/bin/sh
WORKERS=4

bash scripts/migrate.sh

if [ $APP_ENV = "LOCAL" ]
then
    gunicorn --workers=$WORKERS -b 0.0.0.0:8000 wsgi:app --reload --worker-class gevent --timeout 600
else
    gunicorn -b 0.0.0.0:8000 -w $WORKERS wsgi:app --worker-class gevent
fi