---
description: >-
  If you plan to work on CueObserve code and make changes, this documentation
  will give you a high level overview of the components used and how to modify
  them.
---

# Development

### Overview

CueObserve has 5 basic components:

1. Frontend single-page application written on [ReactJS](https://reactjs.org/).
2. Backend based on [Django](https://www.djangoproject.com/) \(python framework\), which is responsible for the communication with the frontend application via REST APIs.
3. [Celery](https://docs.celeryproject.org/) to execute the tasks asynchronously. Tasks like anomaly detection are handled by Celery.
4. [Celery beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html) scheduler to trigger the scheduled tasks.
5. [Redis](https://redis.io/documentation) to handle the task queue of Celery.

### Getting code

Get the code by cloning our open source [github repo](https://github.com/cuebook/cueobserve)

```text
git clone https://github.com/cuebook/CueObserve.git
cd CueObserve
```

### Frontend Development 

The code for frontend is in `/ui` directory. CueObserve uses `npm` as the package manager. 

**Prerequisites:**

1. Node &gt;= 12
2. npm &gt;= 6

```bash
cd ui
npm install    # install dependencies
npm start      # start development server
```

This starts the frontend server on [http://localhost:3000/](https://reactjs.org/)

### Backend Development

The code for the backend is in `/api` directory. As mentioned in the overview it is based on Django framework. 

**Prerequisite:** 

1. Python 3.7
2. PostgreSQL Server running locally or on server \(Optional\)

#### Setup Virtual Environment & Install Dependencies

Setting up a virtual environment is necessary to have your python libraries for this project stored separately so that there is no conflict with other projects. 

```bash
cd api
python3 -m virtualenv myenv         # Create Python3 virtual environment
source myenv/bin/activate           # Activate virtual environment

pip install -r requirements.txt     # Install project dependencies
```

#### Configure environment variables

The environment variables required to run the backend server can be found in `api/.env.dev`. The file looks like below:

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
export IS_AUTHENTICATION_REQUIRED=False 
```

Change the values based on your running PostgreSQL instance. If you do not wish to use PostgreSQL as your database for development, comment lines 4-8 and CueObserve will create a SQLite database file at the location `api/db/db.sqlite3`. 

After changing the values, source the file to initialize all the environment variables. 

```text
source .env.dev
```

Then run the following commands to migrate the schema to your database and load static data required by CueObserve:

```bash
python manage.py migrate                     # Migrate db schema
python manage.py loaddata seeddata/*.json    # Load seed data in database
```

After the above steps are completed successfully, we can start our backend server by running:

```text
python manage.py runserver
```

This starts the backend server on [http://localhost:8000/](https://reactjs.org/). 

#### Celery Development 

CueObserve uses Celery for executing asynchronous  tasks like anomaly detection. There are three components needed to run an asynchronous task, i.e. Redis, Celery and Celery Beat. Redis is used as the message queue by Celery, so before starting Celery services, Redis server should be running. Celery Beat is used as the scheduler and is responsible to trigger the scheduled tasks. Celery workers are used to execute the tasks. 

**Starting Redis Server**

Redis server can be easily started by its official docker image.

```bash
docker run -dp 6379:6379 redis    # Run redis docker on port 6379
```

#### Start Celery Beat

To start celery beat service, activate the virtual environment created for the backend server and then source the .env.dev file to export all required environment variables.

```bash
cd api
source myenv/bin/activate           # Activate virtual environment
source .env.dev                     # Export environment variables.
celery -A app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach         # Run celery beat service
```

#### Start Celery 

To start the celery service, its same as backend or celery beat, first activate the virual env created and then source .env.dev file to export all required environment variables. Celery service doesn't reloads on code changes so we have to install some additional libraries to make it happen. 

```text
cd api
source myenv/bin/activate           # Activate virtual environment
source .env.dev                     # Export environment variables

pip install watchdog pyyaml argh    # Additional libraries to reload celery on code changes
watchmedo auto-restart -- celery -A app worker -l info --purge      # Run celery
```

After these three services are running, you can trigger a task or wait for a scheduled task to run. 

### Building Docker Image

To build the docker image, run the following command in root directory:

```text
docker build -t <YOUR_TAG_NAME> .
```

To run the built image exposed on port 3000:

```text
docker run -dp 3000:3000 <YOUR_TAG_NAME>
```

### Testing

At the moment, we have test cases only for the backend service, test cases for UI are in our roadmap. 

Backend test environment is light and doesn't depend on services like Redis, Celery or Celery-Beat, they are mocked instead. Backend for API and services is tested using [PyTest](https://docs.pytest.org/en/6.2.x/).

 To run the test cases virtual environment should be activated and then source .env.dev file to export all required environment variables. 

```text
cd api
source myenv/bin/activate           # Activate virtual environment
source .env.dev                     # Export environment variables

pytest                              # Run tests
```

