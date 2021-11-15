#!/bin/bash

if [ $# -eq 0 ]
  then
      echo "No arguments supplied"
      exit
fi


cat $1 | psql -U postgres -h 192.168.1.12


rm -vf /tmp/*.csv


PSQL='psql -U postgres -h 192.168.1.12 -d cvat -Atc'

$PSQL 'SELECT 23 as id, username, email, 1 as is_staff, 1 as is_active, password from auth_user where id=1' > /tmp/auth_user.csv


$PSQL 'SELECT email,id,"primary",user_id,verified FROM account_emailaddress' > /tmp/account_emailaddress.csv
$PSQL 'SELECT created,email_address_id,id,key,sent FROM account_emailconfirmation' > /tmp/account_emailconfirmation.csv
$PSQL 'SELECT created,key,user_id FROM authtoken_token' > /tmp/authtoken_token.csv
$PSQL 'SELECT domain,id,name FROM django_site' > /tmp/django_site.csv
$PSQL 'SELECT default_value,id,input_type,label_id,mutable,name,values FROM engine_attributespec' > /tmp/engine_attributespec.csv
$PSQL 'SELECT data_id,file,id FROM engine_clientfile' > /tmp/engine_clientfile.csv
$PSQL 'SELECT chunk_size,compressed_chunk_type,frame_filter,id,image_quality,original_chunk_type,size,start_frame,stop_frame FROM engine_data' > /tmp/engine_data.csv
$PSQL 'SELECT data_id,frame,height,id,path,width FROM engine_image' > /tmp/engine_image.csv
$PSQL 'SELECT assignee_id,id,segment_id,status FROM engine_job' > /tmp/engine_job.csv
$PSQL 'SELECT author_id,id,job_id,message,timestamp,version FROM engine_jobcommit' > /tmp/engine_jobcommit.csv
$PSQL 'SELECT id,name,task_id FROM engine_label' > /tmp/engine_label.csv
$PSQL 'SELECT frame,"group",id,job_id,label_id FROM engine_labeledimage' > /tmp/engine_labeledimage.csv
$PSQL 'SELECT id,image_id,spec_id,value FROM engine_labeledimageattributeval' > /tmp/engine_labeledimageattributeval.csv

$PSQL 'SELECT id,frame,"group",type, (CASE WHEN occluded is true THEN 1 ELSE 0 END) as occluded,z_order,points,job_id,label_id from engine_labeledshape' > /tmp/engine_labeledshape.csv

$PSQL 'SELECT id,shape_id,spec_id,value FROM engine_labeledshapeattributeval' > /tmp/engine_labeledshapeattributeval.csv
$PSQL 'SELECT frame,"group",id,job_id,label_id FROM engine_labeledtrack' > /tmp/engine_labeledtrack.csv
$PSQL 'SELECT id,spec_id,track_id,value FROM engine_labeledtrackattributeval' > /tmp/engine_labeledtrackattributeval.csv
$PSQL 'SELECT created_at,description,maintainer_id,name,updated_at FROM engine_plugin' > /tmp/engine_plugin.csv
$PSQL 'SELECT id,name,plugin_id,value FROM engine_pluginoption' > /tmp/engine_pluginoption.csv
$PSQL 'SELECT assignee_id,bug_tracker,created_date,id,name,owner_id,status,updated_date FROM engine_project' > /tmp/engine_project.csv
$PSQL 'SELECT data_id,file,id FROM engine_remotefile' > /tmp/engine_remotefile.csv
$PSQL 'SELECT id,start_frame,stop_frame,task_id FROM engine_segment' > /tmp/engine_segment.csv
$PSQL 'SELECT data_id,file,id FROM engine_serverfile' > /tmp/engine_serverfile.csv

$PSQL "select id, name, mode, bug_tracker,
       to_char(created_date, 'YYYY-MM-dd HH24:MM:SS') as created_date,
       to_char(updated_date, 'YYYY-MM-dd HH24:MM:SS') as updated_date,
       overlap, segment_size, 
       (CASE WHEN z_order is true then 1 else 0 end) as z_order,
       status, assignee_id, data_id, 23 as owner_id, project_id
       from engine_task" > /tmp/engine_task.csv


$PSQL 'SELECT frame,id,occluded,outside,points,track_id,type,z_order FROM engine_trackedshape' > /tmp/engine_trackedshape.csv
$PSQL 'SELECT id,shape_id,spec_id,value FROM engine_trackedshapeattributeval' > /tmp/engine_trackedshapeattributeval.csv
$PSQL 'SELECT data_id,height,id,path,width FROM engine_video' > /tmp/engine_video.csv
$PSQL 'SELECT lfs,path,status,sync_date,task_id,url FROM git_gitdata' > /tmp/git_gitdata.csv
$PSQL 'SELECT date_joined,extra_data,id,last_login,provider,uid,user_id FROM socialaccount_socialaccount' > /tmp/socialaccount_socialaccount.csv
$PSQL 'SELECT client_id,id,key,name,provider,secret FROM socialaccount_socialapp' > /tmp/socialaccount_socialapp.csv
$PSQL 'SELECT id,site_id,socialapp_id FROM socialaccount_socialapp_sites' > /tmp/socialaccount_socialapp_sites.csv
$PSQL 'SELECT account_id,app_id,expires_at,id,token,token_secret FROM socialaccount_socialtoken' > /tmp/socialaccount_socialtoken.csv

$PSQL 'select id,app_label, model from django_content_type' > /tmp/django_content_type.csv
$PSQL 'select id,name,content_type_id, codename from auth_permission' > /tmp/auth_permission.csv
$PSQL 'select id,name from auth_group' > /tmp/auth_group.csv
