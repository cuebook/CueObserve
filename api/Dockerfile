FROM python:3.9-slim

RUN apt-get update && apt-get install -y build-essential gnupg2 curl libffi-dev libpq-dev gcc default-libmysqlclient-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends unixodbc msodbcsql17 mssql-tools unixodbc-dev
RUN apt-get install -y --no-install-recommends redis-server

WORKDIR /code

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY . ./
RUN chmod +x /code/start_server_new.sh
RUN chown -R www-data:www-data /code
CMD ["/code/start_server_new.sh"]
