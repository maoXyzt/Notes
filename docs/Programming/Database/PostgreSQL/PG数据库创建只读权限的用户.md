# PG数据库创建只读权限的用户

```sql
-- 创建名称为xxxxx的只读用户:
create user xxxxx with password 'pwdxxxxx';
-- 然后把在public这个schema下现有的所有表的select权限赋给readonly用户，并执行下面的SQL命令：
grant select on all tables in schema public to xxxxx;
-- 上面的命令只是把现有的表的权限给了readonly用户，如果此时创建了表，用户还是不能读，需要使用下面的SQL把所建表的select权限也给用户readonly：
alter default privileges in schema public grant select on tables to xxxxx;
```
