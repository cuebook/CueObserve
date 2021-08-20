# Installation

## Install via Docker

```text
docker run -p 3000:3000 cuebook/cueobserve
```

Now visit [localhost:3000](http://localhost:3000) in your browser. 

By default, CueObserve uses sqlite as its database \(not recommended for production use, please refer below to use Postgres as the database for CueObserve\). If you want data to persist across runs, specify a local folder location \(as below\) where db.sqlite3 file can be stored.

```text
docker run -v <local folder location>:/code/db -p 3000:3000 cuebook/cueobserve
```

## Use Postgres as the application database

SQLite is the default storage database for CueObserve. However, it might not be suitable for production. To use Postgres instead, do the following:

Create a `.env` file with given variables:

```text
POSTGRES_DB_SCHEMA=cueobserve
POSTGRES_DB_USERNAME=postgres
POSTGRES_DB_PASSWORD=postgres
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=5432
```

```text
docker run --env-file .env -dp 3000:3000 cuebook/cueobserve
```

In case your Postgres is hosted locally, pass the flag `--network="host"` to connect docker to the localhost of the machine.

## Enabling Authentication

CueObserve comes with built-in authentication \(powered by Django\). To enable authentication, create a `.env` file with the given variables or add these variables in the already created `.env` file with Postgres credentials.

```text
DJANGO_SUPERUSER_USERNAME=<USER_NAME>
DJANGO_SUPERUSER_PASSWORD=<PASSWORD>
DJANGO_SUPERUSER_EMAIL=<YOUR_EMAIL@DOMAIN.COM>
IS_AUTHENTICATION_REQUIRED=True
```

```text
docker run --env-file .env -dp 3000:3000 cuebook/cueobserve
```

If authentication is enabled you can access the [Django Admin](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/) console to do the database operations with a nice UI. To access Django Admin go to [http://localhost:3000/admin](http://localhost:3000/admin) and enter the username and password provided in the `.env` file.

## Infra Requirements

The minimum infrastructure requirement for CueObserve is _1 GB RAM/ 1 CPU_. If Multiple CPUs\(cores\) are provided, they can be utilized by tasks like Anomaly Detection & Root Cause Analysis for faster processing.

