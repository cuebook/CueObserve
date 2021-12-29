---
description: >-
  If you plan to work on CueObserve code and make changes, this documentation
  will give you a high level overview of the components used and how to modify
  them.
---

# Development

### Overview

CueObserve has multi-service architecture, with services as mentioned:

1. `Frontend` single-page application written on [ReactJS](https://reactjs.org). It's code can be found in `ui` folder and runs on [http://localhost:3000/](https://reactjs.org).
2. `API` is based on [Django](https://www.djangoproject.com) (python framework) & uses REST API. It is the main service, responsible for connections, authentication and anomaly.&#x20;
3. `Alerts` micro-service, currently responsible for sending alerting/notifications only to slack. It's code is in `alerts-api` folder and runs on [localhost:8100](http://localhost:8100).
4. [Celery](https://docs.celeryproject.org) to execute the tasks asynchronously. Tasks like anomaly detection are handled by Celery.
5. [Celery beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html) scheduler to trigger the scheduled tasks.
6. [Redis](https://redis.io/documentation) to handle the task queue of Celery.

### Getting code & starting development servers

Get the code by cloning our open source [github repo](https://github.com/cuebook/cueobserve)

```
git clone https://github.com/cuebook/CueObserve.git
cd CueObserve
docker-compose -f docker-compose-dev.yml --env-file .env.dev up --build 
```

`docker-compose`'s build command will pull several components and install them on local, so this will take a few minutes to complete.

### Backend Development

The code for the backend is in `/api` directory. As mentioned in the overview it is based on Django framework.&#x20;

#### Configure environment variables

Configure environment variables as you need for the backend server :

```bash
export ENVIRONMENT=dev

## DB SETTINGS 
export POSTGRES_DB_HOST="localhost"
export POSTGRES_DB_USERNAME="postgres"
export POSTGRES_DB_PASSWORD="postgres"
export POSTGRES_DB_SCHEMA="cue_observe"
export POSTGRES_DB_PORT=5432

## SUPERUSER'S VARIABLE
export DJANGO_SUPERUSER_USERNAME="User"
export DJANGO_SUPERUSER_PASSWORD="admin"
export DJANGO_SUPERUSER_EMAIL="admin@domain.com"

## AUTHENTICATION
export `=False 
```

Change the values based on your running PostgreSQL instance. If you do not wish to use PostgreSQL as your database for development, comment lines 4-8 and CueObserve will create a SQLite database file at the location `api/db/db.sqlite3`.&#x20;

The backend server can be accessed on [http://localhost:8000/](https://www.djangoproject.com).&#x20;

#### Celery Development&#x20;

CueObserve uses Celery for executing asynchronous tasks like anomaly detection. There are three components needed to run an asynchronous task, i.e. Redis, Celery and Celery Beat. Redis is used as the message queue by Celery, so before starting Celery services, Redis server should be running. Celery Beat is used as the scheduler and is responsible to trigger the scheduled tasks. Celery workers are used to execute the tasks.&#x20;

### Testing

At the moment, we have test cases only for the backend service, test cases for UI are in our roadmap.&#x20;

Backend for API and services is tested using [PyTest](https://docs.pytest.org/en/6.2.x/). To run test cases `exec` into cueo-backend and run command

```
pytest
```
