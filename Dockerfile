FROM python:3.12-alpine AS builder

ENV POETRY_VERSION=2.1.4

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    sqlite-dev \
    curl

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry==$POETRY_VERSION && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

FROM python:3.12-alpine

RUN apk add --no-cache \
    libffi \
    sqlite \
    curl

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY ./app /app/app
COPY .env /app/.env

RUN mkdir -p /app/data
