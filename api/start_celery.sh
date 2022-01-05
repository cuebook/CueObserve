#!/usr/bin/env bash
# start-celery.sh

(celery -A app worker --concurrency=2 -l -n main INFO --purge) &
(celery -A app worker --concurrency=4 -Q anomalySubTask -n sub -l INFO --purge) 
