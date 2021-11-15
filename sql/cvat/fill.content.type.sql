drop table if exists auth_permission_tmp;
drop table if exists django_content_type_tmp;
CREATE TABLE `django_content_type_tmp` (  
`id` int(11) NOT NULL AUTO_INCREMENT,  
`app_label` varchar(100) NOT NULL,  
`model` varchar(100) NOT NULL,  
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `auth_permission_tmp` (  
`id` int(11) NOT NULL AUTO_INCREMENT,  
`name` varchar(255) NOT NULL,  
`content_type_id` int(11) NOT NULL,  
`codename` varchar(100) NOT NULL,  
PRIMARY KEY (`id`),  
UNIQUE KEY `UK__auth_permission_tmp_uniqXXX` (`content_type_id`,`codename`),  
CONSTRAINT `FK__auth_permission_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type_tmp` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;


LOAD DATA LOCAL INFILE '/tmp/django_content_type.csv' 
REPLACE INTO TABLE django_content_type_tmp
FIELDS TERMINATED BY '|'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(id, app_label, model);

LOAD DATA LOCAL INFILE '/tmp/auth_permission.csv' 
REPLACE INTO TABLE auth_permission_tmp
FIELDS TERMINATED BY '|'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(id, name, content_type_id, codename);


insert into django_content_type (app_label, model)
select D1.app_label, D1.model
from django_content_type_tmp D1
left join django_content_type D0 on D1.app_label=D0.app_label and D1.model = D0.model
where D0.id is null
order by D1.app_label, D1.model;


insert into auth_permission (name, content_type_id, codename)
select A1.name, DCT.id as content_type_id, A1.codename
from auth_permission_tmp A1
left join auth_permission A0 on A1.name = A0.name and A1.codename=A0.codename
left join django_content_type DCT on A1.content_type_id = DCT.id
where A0.id is null


drop table if exists auth_permission_tmp;
drop table if exists django_content_type_tmp;
