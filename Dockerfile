FROM python:3.7.3-alpine3.9
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

WORKDIR /
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv ; pipenv install

COPY . /
WORKDIR /app