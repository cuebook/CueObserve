FROM python:3.9-slim-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . .
CMD python3 run.py