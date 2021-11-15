SELECT * FROM
  (SELECT
      CONCAT(cl.TABLE_NAME, ' [', cl.COLUMN_NAME, ', ', cl.COLUMN_TYPE, ']') tableRowType
    FROM information_schema.columns cl,  information_schema.TABLES ss
    WHERE
      cl.TABLE_NAME = ss.TABLE_NAME AND
      cl.TABLE_SCHEMA = @firstDatabaseName AND
      ss.TABLE_TYPE IN('BASE TABLE', 'VIEW')
    ORDER BY
      cl.table_name ) AS t1
LEFT JOIN
  (SELECT
      CONCAT(cl.TABLE_NAME, ' [', cl.COLUMN_NAME, ', ', cl.COLUMN_TYPE, ']') tableRowType
    FROM information_schema.columns cl,  information_schema.TABLES ss
    WHERE
      cl.TABLE_NAME = ss.TABLE_NAME AND
      cl.TABLE_SCHEMA = @secondDatabaseName AND
      ss.TABLE_TYPE IN('BASE TABLE', 'VIEW')
    ORDER BY
      cl.table_name ) AS t2 ON t1.tableRowType = t2.tableRowType
WHERE
  t2.tableRowType IS NULL
UNION
SELECT * FROM
  (SELECT
      CONCAT(cl.TABLE_NAME, ' [', cl.COLUMN_NAME, ', ', cl.COLUMN_TYPE, ']') tableRowType
    FROM information_schema.columns cl,  information_schema.TABLES ss
    WHERE
      cl.TABLE_NAME = ss.TABLE_NAME AND
      cl.TABLE_SCHEMA = @firstDatabaseName AND
      ss.TABLE_TYPE IN('BASE TABLE', 'VIEW')
    ORDER BY
      cl.table_name ) AS t1
RIGHT JOIN
  (SELECT
      CONCAT(cl.TABLE_NAME, ' [', cl.COLUMN_NAME, ', ', cl.COLUMN_TYPE, ']') tableRowType
    FROM information_schema.columns cl,  information_schema.TABLES ss
    WHERE
      cl.TABLE_NAME = ss.TABLE_NAME AND
      cl.TABLE_SCHEMA = @secondDatabaseName AND
      ss.TABLE_TYPE IN('BASE TABLE', 'VIEW')
    ORDER BY
      cl.table_name ) AS t2 ON t1.tableRowType = t2.tableRowType
WHERE
  t1.tableRowType IS NULL;

drop table engine_pluginoption;
drop table engine_plugin;

alter table auth_user modify column first_name varchar(150);
alter table engine_data add column storage_method varchar(15);
alter table engine_label add column color varchar(8) after name;
alter table engine_labeledimage add column source varchar(16) after `group`;
alter table engine_labeledshape add column source varchar(16) after `group`;
alter table engine_labeledtrack add column source varchar(16) after `group`;

