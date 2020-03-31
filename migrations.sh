#!/bin/sh
MAX_RETRIES=5
WORKERS=4
RETRIES=0
until flask db upgrade; do
    RETRIES=`expr $RETRIES + 1`
    if [[ "$RETRIES" -eq "$MAX_RETRIES" ]]; then
        echo "Retry Limit Exceeded. Aborting..."
        exit 1
    fi
    sleep 2
done