# Installation

## Install via Docker

```
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/docker-compose.yml -q -O cueobserve-docker-compose.yml
docker-compose -f cueobserve-docker-compose.yml up -d
```

Now visit [localhost:3000](http://localhost:3000) in your browser. 

## Use Postgres as the application database

SQLite is the default storage database for CueObserve. However, it might not be suitable for production. To use Postgres instead, do the following:

Create a `.env` file with given variables:

```
POSTGRES_DB_SCHEMA=cueobserve
POSTGRES_DB_USERNAME=postgres
POSTGRES_DB_PASSWORD=postgres
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=5432
```

```
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/docker-compose.yml -q -O cueobserve-docker-compose.yml
docker-compose --env-file .env -f cueobserve-docker-compose.yml up -d
```

## Authentication

CueObserve comes with built-in authentication (powered by Django). By default authentication is disabled, to enable authentication create a `.env` file with the given variables or add these variables in the already created `.env` file with Postgres credentials.

```
DJANGO_SUPERUSER_USERNAME=<USER_NAME>
DJANGO_SUPERUSER_PASSWORD=<PASSWORD>
DJANGO_SUPERUSER_EMAIL=<YOUR_EMAIL@DOMAIN.COM>
IS_AUTHENTICATION_REQUIRED=True
```

```
wget https://raw.githubusercontent.com/cuebook/CueObserve/latest_release/docker-compose.yml -q -O cueobserve-docker-compose.yml
docker-compose --env-file .env -f cueobserve-docker-compose.yml up -d
```

If authentication is enabled you can access the [Django Admin](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/) console to do the database operations with a nice UI. To access Django Admin go to [http://localhost:3000/admin](http://localhost:3000/admin) and enter the username and password provided in the `.env` file.

## Email Notification

CueObserve comes with built-in email alert notification system(powered by Django). By default email notifications are disabled, to enable notifications create a `.env` file with the given variables or add these variables in the already created `.env` file.

```
EMAIL_HOST="smtp.gmail.com" 
EMAIL_HOST_USER=<YOUR_EMAIL@gmail.com>
EMAIL_HOST_PASSWORD=<YOUR_EMAIL_PASSWORD>
```

Allow less secure apps: ON for your given EMAIL_HOST_USER email Id, click on [enable access to less secure app](https://myaccount.google.com/lesssecureapps?pli=1\&rapt=AEjHL4N7wse3vhCsvRv-aWy8kKeEGDZS2YDbW1SfTL17HVhtemi7zZW5gzbZSBnrNgknL_gPBDn3xVo0qUj-W6NuaYTSU7agQQ)

Unlock Captcha for your gmail account, click on [Unlock Captcha](https://accounts.google.com/b/0/UnlockCaptcha)



## Infra Requirements

The minimum infrastructure requirement for CueObserve is _1 GB RAM/ 1 CPU_. If Multiple CPUs(cores) are provided, they can be utilized by tasks like Anomaly Detection & Root Cause Analysis for faster processing.
