pg的自增主键是通过序列维护的，序列不可以直接赋值，
向库中插入的数据包含自增的主键值后，用下述命令设置自增主键的值：
```sql
SELECT SETVAL('authent_user_id_seq', (SELECT max(id) FROM authent_user));
```

当清空表后，用以下命令重置序列的值：
```sql
ALTER SEQUENCE authent_user_id_seq RESTART WITH 1;
```
