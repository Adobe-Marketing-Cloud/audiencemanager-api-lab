#!/bin/sh
set -e
echo "Resetting Database..."
echo
echo ">> Deleting old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
echo
echo ">> Deleting database"
find . -name "db.sqlite3" -delete
echo
echo ">> Running manage.py makemigrations"
python manage.py makemigrations
echo
echo ">> Running manage.py migrate"
python manage.py migrate
echo
#echo ">> Loading initial data"
#python manage.py loaddata initial_data.json
echo ">> Enter password for creating the initial 'admin' user"
echo "Username: admin"
python manage.py createsuperuser --username admin --email ''
echo
echo ">> Done"
echo
