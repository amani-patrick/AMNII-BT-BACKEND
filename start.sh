#!/bin/bash
python manage.py migrate
gunicorn amnii_bt.wsgi:application --bind 0.0.0.0:$PORT

