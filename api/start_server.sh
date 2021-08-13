#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
redis-server &
export DEBUG=false
python manage.py migrate
python manage.py loaddata seeddata/*.json
chmod -R 777 db/db.sqlite3
chown -R www-data:www-data db/db.sqlite3
(gunicorn app.wsgi --user www-data --bind 0.0.0.0:8000 --workers 3 --timeout 300) &
(celery -A app worker --concurrency=6 -l INFO --purge) &
(celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler) &
(/user/bin/redis-server)
nginx -g "daemon off;"
