#!/usr/bin/env bash
# start-server.sh
export DEBUG=false
python manage.py migrate
python manage.py loaddata seeddata/*.json
if  [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --noinput)
fi
chmod -R 777 db
chown -R www-data:www-data db
python ./manage.py collectstatic
mkdir -p /home/staticfiles
mv static_root/* /home/staticfiles
rm -rf static_root/
(celery -A app worker --concurrency=2 -l INFO --purge) &
(celery -A app worker --concurrency=4 -Q anomalySubTask -l INFO --purge) &
(celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler) &
python manage.py shell -c  "from anomaly.runTelemetry import create_installation_userId; create_installation_userId()" &

gunicorn app.wsgi --reload --user www-data --bind 0.0.0.0:8000 --workers 3 --timeout 300