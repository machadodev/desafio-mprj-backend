# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install psycopg2-binary djangorestframework-xml
COPY ./requirements.txt .
COPY ./dev-requirements.txt .
RUN pip install -r dev-requirements.txt

# copy project
COPY . .
