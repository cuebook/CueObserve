---
description: Commands for installation and running services for development
---

# Development

### UI 

CueObserve's UI is `javascript` based. It's built using reactjs, a JavaScript library for building user interfaces. The code for UI can be found in `ui/` directory.

#### Setup & Start UI server

```text
cd ui    # go to ui directory
npm i    # install dependencies
npm start    # start development server
```

The UI server by default runs on [http://localhost:3000/](https://reactjs.org/)

### Backend 

CueObserve's backend is `python3.7` based. It incorporates Django, a high-level Python Web framework .  Celery is used for running tasks like Anomaly Detection, scheduled or ran manually, which can be time consuming and run out of the request-response cycle. Celery Beat is used as a scheduler and Redis is a requirement for celery. The code for backend can be found in `api/` directory.

#### Backend Setup 

Prerequisite: `python3.7`

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



