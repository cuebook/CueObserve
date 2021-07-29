# Installation

## Install via Docker

```text
docker run -p 3000:3000 cuebook/cueobserve
```

Now visit [localhost:3000](http://localhost:3000) in your browser. 

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

In case your postgres is hosted locally, pass flag `--network="host"` to connect docker to localhost of machine.

