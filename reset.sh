#!/bin/bash

if [ $# -eq 0 ]
  then
      echo "do: ./reset.sh username email password"
      exit
fi
username=$1
email=$2
pass=$3


find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
mysql -e "drop database brainsharer;create database brainsharer;"
python manage.py makemigrations
python manage.py makemigrations authentication
python manage.py makemigrations brain
python manage.py makemigrations neuroglancer
python manage.py showmigrations
python manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$username', '$email', '$pass')" | python manage.py shell

# inserts
mysql brainsharer < ./sql/brainsharer.inserts.sql
mysql brainsharer < ./sql/secrets.sql
