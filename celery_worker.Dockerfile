FROM python:3.6-alpine

MAINTAINER devops
WORKDIR /mon/


RUN apk add --update  postgresql-dev git \
    libevent-dev libffi-dev openssl yaml linux-headers build-base python3 jpeg-dev zlib-dev && \
    pip3 install uwsgi
ADD ./requirements.txt /

RUN pip3 install -r /requirements.txt
ADD . /mon/

COPY ./docker_settings.py /mon/mon/monserver/settings.py
WORKDIR /mon/mon/

CMD ["celery", "-A", "monserver.celery", "worker","-l","debug","-f","celery.logs"]
