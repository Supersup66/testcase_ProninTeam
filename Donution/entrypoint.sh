#!/bin/bash

set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Creating migrations..."
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

exec "$@"