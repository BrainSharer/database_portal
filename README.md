### Setup the database portal on your local machine
1. Get repo: `git clone git@github.com:BrainSharer/database_portal.git`
1. Create a virtual environment in your home dir: python3 -m venv /usr/local/share/brainsharer
1. cd database_portal
1. `source /usr/local/share/brainsharer/bin/activate`
1. Upgrade pip: `pip install -U pip`
1. run: `pip install -r requirements.txt`
1. On MacOS you might need to do this: 
`CFLAGS="-I$(brew --prefix)/include" LDFLAGS="-L$(brew --prefix)/lib" pip install mysqlclient`
1. On ubuntu/debian, as root install libmysqlclient-dev
1. As root go into mysql and do:
    1. `create database brainsharer;`
    1. `CREATE USER 'brainsharer'@'localhost' IDENTIFIED BY 'CHANGME'`;
    1. `grant all privileges on brainsharer.* to 'brainsharer'@'localhost' WITH GRANT OPTION;`
    1. `update user set Super_Priv='Y' where user='brainsharer';`
    1. `flush privileges;`
1. Make the Django database migrations:
    1. `python manage.py check`
    1. `python manage.py makemigrations`
    1. `python manage.py showmigrations` # there should be migrations
    for admin, auth, brain, contenttypes, neuroglancer and sessions.
    If not you might need to do something like `python manage.py
    makemigrations neuroglancer`
1. Create a superuser: `python manage.py createsuperuser`
1. Create a view from the existing tables with the script in the sql
dir with `mysql brainsharer < sql/create_sections.sql`

## To redo all database migrations and start from scratch
1. go to the top level dir of the project (same dir as the manage.py script)
1. run: `find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`
1. run: `find . -path "*/migrations/*.pyc"  -delete`
1. go to the mysql/mariadb prompty and delete and recreate the database:
    1. `drop database brainsharer`
    1. `create database brainsharer`
1. rerun the migrations as above.
