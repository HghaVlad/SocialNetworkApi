#!/bin/sh

python social_network/manage.py makemigrations
python social_network/manage.py migrate
python social_network/manage.py runserver $SERVER_ADDRESS

exec "$@"