FROM python:3.7.3-alpine3.10

COPY requirements/flower_app.txt /celery_app/requirements/flower_app.txt

RUN pip install --upgrade pip

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && pip install -r /celery_app/requirements/flower_app.txt \
  && apk del build-deps

WORKDIR /celery_app

COPY . /celery_app

CMD ["celery", "-A", "app.tasks", "flower"]
