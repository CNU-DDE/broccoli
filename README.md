# Injik/Broccoli

Microservice sub-repository for injik/Broccoli user management engine

## Prerequisite

To develop Injik/Broccoli, the followings are required:

- Python related: `python3`, `pip3` and `pipenv`
- MySQL / MariaDB
- Injik/did-core

You can prepare *MariaDB* and *did-core* with pre-defined
`docker-compose.yaml` in [here](https://github.com/CNU-DDE/broccoli/blob/main/examples/docker-compose.dev.yaml)

## Environment variables

```bash
MARIADB_HOST # MariaDB hostname
MARIADB_PORT # MariaDB port
MARIADB_USER # MariaDB username
MARIADB_PASSWORD # MariaDB password
MARIADB_DATABASE # MariaDB database name
RUNMODE # Run mode - one of `production` or `development`
DID_HOST # did-core service hostname
DID_PORT # did-core service port
JWT_SECR # JWT signing secret
FE_HOST # API server frontend host
CORS_ALLOWED_HOST # CORS allowed origin
CORS_ALLOWED_LOCAL_PORT # CORS allowed port for `localhost`
```

## Code development

1. Entering python virtual environment:

```bash
pipenv shell
```

1. Install dependencies:

```bash
# In virtual environment (broccoli)
pipenv install
```

1. Migrate to database

```bash
# In virtual environment (broccoli)
python manage.py makemigrations app
python manage.py makemigrations
python manage.py migrate app
python manage.py migrate
```

1. Run

```bash
# In virtual environment (broccoli)
python manage.py runserver
```

## Usage

As Injik/broccoli is designed to use as a Kubernetes pod,
it's packaged as a Docker image.

You can find and use it in [Docker hub](https://hub.docker.com/r/haeramkeem/broccoli)

Here's example of how to run a container:

```bash
docker run -d \
-p 60072:7772 \
-h 0.0.0.0 \
-e ${environments ...} \
haeramkeem/brccoli
```

Also, `docker-compose.yaml` file for easy-to-use container deployment is prepared
in [here](https://github.com/CNU-DDE/broccoli/blob/main/examples/docker-compose.yaml)
