use cvat_db;

truncate table engine_data;
truncate table engine_job;
truncate table engine_labeledshape;
truncate table engine_segment;
truncate table engine_task;
truncate table engine_label;

LOAD DATA LOCAL INFILE '/tmp/auth_user.csv' 
REPLACE INTO TABLE auth_user
FIELDS TERMINATED BY '|'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
( id, username, email, is_staff, is_active, password);


LOAD DATA LOCAL INFILE '/tmp/engine_label.csv' 
REPLACE INTO TABLE engine_label
FIELDS TERMINATED BY '|'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';



LOAD DATA LOCAL INFILE '/tmp/engine_data.csv' 
REPLACE INTO TABLE engine_data
FIELDS TERMINATED BY '|'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';


LOAD DATA LOCAL INFILE '/tmp/engine_task.csv' 
REPLACE INTO TABLE engine_task
FIELDS TERMINATED BY '|'
-- OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(id, name, mode, bug_tracker,created_date,updated_date,
       overlap, segment_size, z_order,status, @vassignee_id, data_id, owner_id, @vproject_id)
SET assignee_id = NULLIF(@vassignee_id,''),
project_id = NULLIF(@vproject_id,'');
       
LOAD DATA LOCAL INFILE '/tmp/engine_segment.csv' 
REPLACE INTO TABLE engine_segment
FIELDS TERMINATED BY '|'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA LOCAL INFILE '/tmp/engine_job.csv' 
REPLACE INTO TABLE engine_job
FIELDS TERMINATED BY '|' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(id,segment_id,@vassignee_id,status)
SET assignee_id = NULLIF(@vassignee_id,'');

LOAD DATA LOCAL INFILE '/tmp/engine_labeledshape.csv' 
REPLACE INTO TABLE engine_labeledshape
FIELDS TERMINATED BY '|' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(`id`,`frame`,`group`,`type`,`occluded`,`z_order`,`points`,`job_id`,`label_id`);
