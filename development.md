---
description: Commands for installation and running services for development
---

# Development

### UI

CueObserve's UI is built using 

\[gitbook landing page\]\(https://www.gitbook.com/book/seadude/linking/details\)

  
, it's code can be found at `ui/`

#### Setup & Start UI server

```text
cd ui    # go to ui directory
npm i    # install dependencies
npm start    # start development server
```

#### Backend Setup 

Requirements: `python3.7`

Note: Before running any command in `api` directory ensure you have python3.7 as `source`, as below:

```text
cd api    # go to api directory
python3.7 -m virtualenv myenv    # make python3.7 virtual environment
source myenv/bin/activate         # activate virtual environment

pip install -r requirements.txt     # install dependencies

# Installations for celery 
pip install watchdog
pip install pyyaml
pip install argh

python manage.py migrate
python manage.py loaddata seeddata/*.json
```

#### Start Backend Server

```text
python manage.py runserver
```



Celery is used for running scheduled tasks like Anomaly Detection and is also used when tasks are ran manually. Redis is a requirement for celery.

#### Run Redis via Docker

```text
docker run -dp 6379:6379 redis
```

#### Run Celery Beat 

```text
celery -A app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

#### Run Celery  

```text
watchmedo auto-restart -- celery -A app worker -l info        # celery => 5.0
```



