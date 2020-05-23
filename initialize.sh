#!/bin/sh
# Reference: createsuperuser: https://docs.djangoproject.com/en/3.0/ref/django-admin/#createsuperuser
# Reference: multiple scripts in postdeploy: https://stackoverflow.com/a/46221729/13193202

python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py shell --command="from utils.rule_helper import auto_detect_heroku_apps; auto_detect_heroku_apps()"