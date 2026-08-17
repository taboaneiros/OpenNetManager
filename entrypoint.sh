#!/bin/sh
set -e

echo "Waiting for database to be ready..."
sleep 5

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting application..."
exec "$@"
