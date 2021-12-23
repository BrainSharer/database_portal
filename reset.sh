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

mysql brainsharer -e "insert into authentication_lab (lab_name,active,created,lab_url) values ('Princeton',1,NOW(),'https://princeton.edu')"
mysql brainsharer -e "insert into authentication_lab (lab_name,active,created,lab_url) values ('UCSD',1,NOW(),'https://activebrainatlas.ucsd.edu/data')"
mysql brainsharer -e "insert into authentication_lab (lab_name,active,created,lab_url) values ('Duke',1,NOW(),'https://duke.edu')"

mysql brainsharer -e "insert into animal (animal,active,created) values ('DK52',1,NOW())"
# input types
mysql brainsharer -e "insert into input_type (input_type,description,active,created,updated) values ('manual','Data entered by user in Neuroglancer',1,NOW(),NOW())"
mysql brainsharer -e "insert into input_type (input_type,description,active,created,updated) values ('detected','Data created by scripts',1,NOW(),NOW())"
# structure
mysql brainsharer -e "insert into structure (abbreviation,description,active,created) values ('point','Point data described by x,y,z',1,NOW())"
