FROM python:3.7.7-buster

RUN apt-get update

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc musl-dev libffi-dev libssl-dev libxft-dev

RUN apt-get -y install python3-dev

#RUN apt-get g++
RUN apt-get update \
    && apt-get -y install gfortran libopenblas-dev liblapack-dev \
	&&  pip install --no-cache-dir --upgrade pip \
	&&  pip install numpy==1.20.2 \
	&&  pip install scipy==1.6.2 \
	&&  pip install pandas==1.1.0 \
  &&  pip install pystan==2.19.1.1 \
  &&  pip install convertdate \
	&&  pip install prophet

#AWS Instructions
RUN apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev


RUN mkdir -p /lambda_anomaly_detection

COPY . /lambda_anomaly_detection

RUN pip install \
        --target /lambda_anomaly_detection \
        awslambdaric

WORKDIR /lambda_anomaly_detection


ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

CMD [ "cloudwrapper.aws_lambda_handler" ]