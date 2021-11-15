### CVAT migration from Postgres into existing Django Mysql project
#### Libraries
1. pip install git+https://github.com/openvinotoolkit/datumaro@v0.1.0
1. diskcache
1. logstash
#### Mysql database modifications
1. alter table auth_user modify column first_name varchar(150)
1. drop table engine_plugin
1. drop table engine_pluginoption
1. alter table engine_data add column storage_method varchar(15)

### Postgres to Mysql in Docker
# alter FKs on active_atlas_development
`alter table auth_group_permissions drop foreign key auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE auth_group_permissions ADD CONSTRAINT FK__AGP_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) ON UPDATE CASCADE;


alter table auth_user_groups drop foreign key auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE auth_user_groups ADD CONSTRAINT FK__AUG_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) ON UPDATE CASCADE;`
1. Update tables
`update auth_group set id = 7 where id = 1;
update auth_group set id = 1 where id = 2;
update auth_group set id = 2 where id = 3;
update auth_group set id = 3 where id = 4;
update auth_group set id = 4 where id = 5;
-- kui
insert into auth_user_groups (user_id, group_id) values (23,1);

select * from auth_group
order by id;

select AU.id, AU.username, AG.id as group_id, AG.name
from auth_group AG
inner join auth_user_groups AUG on AG.id = AUG.group_id
inner join auth_user AU on AUG.user_id = AU.id;`
### Save existing docker containers from muralis
1. docker save -o cvat_ui.tar cvat_cvat_ui:latest
### Load muralis docker image
1. docker load -i cvat_ui.tar

1. Enter the cvat container `docker exec -u 0 -it cvat bash` and:
    1. apt-get update
    1. apt install libmysqlclient-dev vim
    1. pip install -U pip
    1. apt install build-essential
    1. pip install django-mysql mysqlclient
    1. edit supervisor.conf and change postgres port to mysql and remove migrate
        1. change 5432 to 3306
        1. remove the migration at line 62
    1. vi cvat/settings/production.py and add mysql settings
`
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'active_atlas_development',                      # Or path to database file if using sqlite3.
        'USER': 'dklab',                      # Not used with sqlite3.
        'PASSWORD': '$pw4dklabdb',                  # Not used with sqlite3.
        'HOST': '192.168.1.12',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',    # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'sql_mode': 'traditional'},
    }
}
`
1. remove migrations:
`find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete`
1. test with `python3 manage.py check`
1. exit cvat container 
1. get container ID of cvat with `docker ps`
1. commit `docker commit container_id cvat_mysql:latest`
1. edit docker.compose.yml and remove cvat_db service and all references to it.
1. change container_name and image_name from cvat to cvat_mysql
1. changes references of CVAT_POSTGRES_HOST to point to db.dk.ucsd.edu
1. turn down docker: `docker-compose down`
1. run `docker-compose up -d`
## Problems
1. Bad Gateway, make sure table django_site points to same name as host in docker-compose.override.yml
1. Keeps building cvat_ui - make sure container and image for cvat_ui are the same as in `docker container ls`
### Upgrading
1. save existing images as v1: `docker commit a7c40625961  cvat_mysql:v1`
1. To run with that v1 image, edit docker-compose.yml and add the ':v1' tag to the image
