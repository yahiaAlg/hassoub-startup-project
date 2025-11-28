#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Populate database with initial data
python manage.py populate_pages
python manage.py populate_lessons
python manage.py populate_achievements