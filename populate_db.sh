#!/usr/bin/env bash

# Populate database with initial data
# python manage.py populate_lessons
python manage.py populate_pages
python manage.py enhanced_lessons
python manage.py populate_scenarios
python manage.py populate_achievements
python manage.py createsuperuser 

