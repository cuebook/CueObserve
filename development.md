---
description: Commands for installation and running services for development
---

# Development

### UI 

CueObserve's UI is `javascript` based. It's built using reactjs, a JavaScript library for building user interfaces. The code for UI can be found in `ui/` directory.

#### Setup & Start UI server

```text
cd ui
npm install    # install dependencies
npm start      # start development server
```

This starts UI server on [http://localhost:3000/](https://reactjs.org/)

### Backend 

CueObserve's backend is `python3.7` based. It incorporates Django, a high-level Python Web framework .  Celery is used for running tasks like Anomaly Detection, scheduled or ran manually, which can be time consuming and run out of the request-response cycle. Celery Beat is used as a scheduler and Redis is a requirement for celery. The code for backend can be found in `api/` directory.

Prerequisite: `python3.7`

Note: Before running any command in `api` directory ensure you have python3.7 as `source`, as below:

#### Backend Setup

```text
cd api
python3.7 -m virtualenv myenv       # make python3.7 virtual environment
source myenv/bin/activate           # activate virtual environment

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

This starts the server on [http://localhost:8000/](https://reactjs.org/). 

#### Install & Run Redis 

Install and run redis-server \([https://redis.io/topics/quickstart](https://redis.io/topics/quickstart)\) or using docker

```text
docker run -dp 6379:6379 redis    # run redis
```

#### Start Celery Beat 

Celery Beat is a scheduler. Read more at [https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#:~:text=celery%20beat%20is%20a%20scheduler,entries%20in%20a%20SQL%20database.)

```text
celery -A app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach         # run celery beat
```

#### Start Celery 

Celery is a task queue implementation for Python web applications used to asynchronously execute work outside the HTTP request-response cycle. Read more at [https://docs.celeryproject.org/en/stable/](https://docs.celeryproject.org/en/stable/)

```text
watchmedo auto-restart -- celery -A app worker -l info       # run celery => 5.0
```

### Optional

#### Using Postgres as application db

SQLite is the default storage database for CueObserve. However, if you want to use Postgres instead, do the following:

Create a `.env.dev` file with given variables:

```text
export POSTGRES_DB_SCHEMA=cueobserve
export POSTGRES_DB_USERNAME=postgres
export POSTGRES_DB_PASSWORD=postgres
export POSTGRES_DB_HOST=localhost
export POSTGRES_DB_PORT=5432
```

And then source these variables before running backend commands

```text
source .env.dev
```

