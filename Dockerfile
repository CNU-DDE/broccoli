FROM python:3.8-slim

LABEL name="Haeram Kim"
LABEL email="haeram.kim1@gmail.com"
LABEL image_version="1.0.0"
LABEL app_version="1.0.0"
LABEL description="Injik/broccoli API server image"

ENV VAR1=10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN DEBIAN_FRONTEND="noninteractive" \
    apt-get update && \
    apt-get install -y \
    gcc \
    default-libmysqlclient-dev

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /etc/injik/broccoli
COPY . /etc/injik/broccoli

RUN adduser -u 5678 --disabled-password --gecos "" injik && chown -R injik /etc/injik/broccoli
USER injik

ENTRYPOINT [ "/etc/injik/broccoli/docker-entrypoint.sh" ]
