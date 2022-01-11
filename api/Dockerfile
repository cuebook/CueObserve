FROM cuebook/cue-observe-backend:base

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./
RUN chmod +x /code/start_server_new.sh
RUN chmod +x /code/start_celery.sh
RUN chown -R www-data:www-data /code
CMD ["/code/start_server_new.sh"]
