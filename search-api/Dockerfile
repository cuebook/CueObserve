FROM python:3.9-slim-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["/code/entrypoint.sh"] 
CMD ["python", "manage.py", "run", "--port", "8200"]