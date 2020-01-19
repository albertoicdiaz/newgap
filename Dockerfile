FROM python:3.7-alpine
MAINTAINER Alberto Calvo

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./users /users

RUN adduser -D user
USER user
