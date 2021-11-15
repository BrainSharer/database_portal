alter table auth_group_permissions drop foreign key auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE auth_group_permissions ADD CONSTRAINT FK__AGP_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) ON UPDATE CASCADE;


alter table auth_user_groups drop foreign key auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE auth_user_groups ADD CONSTRAINT FK__AUG_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) ON UPDATE CASCADE;



update auth_group set id = 7 where id = 1;
update auth_group set id = 1 where id = 2;
update auth_group set id = 2 where id = 3;
update auth_group set id = 3 where id = 4;
update auth_group set id = 4 where id = 5;
-- kui
insert into auth_user_groups (user_id, group_id) values (23,1);


select AU.id, AU.username, AG.id as group_id, AG.name
from auth_group AG
inner join auth_user_groups AUG on AG.id = AUG.group_id
inner join auth_user AU on AUG.user_id = AU.id;

