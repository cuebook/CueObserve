#!/usr/bin/env bash
# start-celery.sh

(celery -A app worker --concurrency=2 -n main -l INFO --purge) &
(celery -A app worker --concurrency=4 -Q anomalySubTask -n sub -l INFO --purge) 
