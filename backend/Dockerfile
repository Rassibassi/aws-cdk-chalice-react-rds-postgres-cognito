FROM python:3.9.5-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

COPY ./requirements.txt .
COPY ./requirements-dev.txt .
RUN pip install chalice && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh