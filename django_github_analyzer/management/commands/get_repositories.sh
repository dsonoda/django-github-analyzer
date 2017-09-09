#!/bin/bash
export DJANGO_SETTINGS_MODULE=mysite.settings
. /vagrant/venv/bin/activate
cd /path/to/src
python manage.py some_command
