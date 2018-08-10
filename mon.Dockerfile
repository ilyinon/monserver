FROM python:3.6-alpine

MAINTAINER devops
WORKDIR /mon/


RUN apk add --update  postgresql-dev git \
    libevent-dev libffi-dev openssl yaml linux-headers build-base python3 jpeg-dev zlib-dev && \
    pip3 install uwsgi

ADD . /mon/
COPY /mon/docker_settings.py /mon/monserver/settings.py

RUN pip3 install -r /mon/requirements.txt

CMD sh /mon/entrypoint.sh