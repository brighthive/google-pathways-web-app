#!/bin/sh
# MAX_RETRIES=5
WORKERS=4
# RETRIES=0
# until flask db upgrade; do
#     RETRIES=`expr $RETRIES + 1`
#     if [[ "$RETRIES" -eq "$MAX_RETRIES" ]]; then
#         echo "Retry Limit Exceeded. Aborting..."
#         exit 1
#     fi
#     sleep 2
# done

flask db upgrade && gunicorn --workers=$WORKERS -b 0.0.0.0:8000 wsgi:app --reload --worker-class gevent --timeout 600