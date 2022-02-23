#!/usr/bin/env bash
# start-celery.sh

celery -A app worker --concurrency=2 -l INFO &
celery -A app worker --concurrency=4 -Q anomalySubTask -l INFO 
