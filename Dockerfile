# build environment
FROM node:12-slim as builder
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ui/package.json /app/package.json
RUN npm install --silent
COPY ui /app

RUN npm run build



# compile-image
FROM python:3.7-slim-buster AS compile-image
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends build-essential gcc default-libmysqlclient-dev libodbc1 unixodbc unixodbc-dev


RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY api/requirements.txt .
RUN pip install -r requirements.txt



# production environment
FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED=1
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y gnupg2 curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends unixodbc msodbcsql17 mssql-tools unixodbc-dev
RUN apt-get install -y --no-install-recommends redis-server nginx default-libmysqlclient-dev 

WORKDIR /code
COPY api /code/
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN chmod +x /code/start_server.sh
RUN chown -R www-data:www-data /code

EXPOSE 3000
STOPSIGNAL SIGTERM
CMD ["/code/start_server.sh"]
