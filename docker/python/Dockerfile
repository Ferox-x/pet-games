FROM python:3.10-alpine as builder

WORKDIR /srv/www/app_project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../../requirements_prod.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /srv/www/app_project/wheels -r requirements_prod.txt


FROM python:3.10-alpine

WORKDIR /srv/www/app_project

COPY --from=builder  /srv/www/app_project/wheels /wheels
COPY . .

RUN pip install --no-cache /wheels/*
