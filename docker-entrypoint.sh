#!/bin/bash

for i in $(seq 1 5); do
    echo "Waiting for MariaDB to start up... ($i)"
    sleep 1
done

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate app
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:7772
