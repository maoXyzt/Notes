# PG 设置自增序列值

PostgreSQL 的自增主键是通过序列维护的，序列不可以直接赋值。

## 1. 设置序列的值

向库中插入的数据包含自增的主键值后，用下述命令设置自增主键的值。

假设表名为 `authent_user`，主键名为 `id`，序列名为 `authent_user_id_seq`，则用以下命令设置序列的值：

```sql
SELECT SETVAL('authent_user_id_seq', (SELECT max(id) FROM authent_user));
```

## 2. 重置序列的值

当清空表后，用以下命令重置序列的值：

```sql
ALTER SEQUENCE authent_user_id_seq RESTART WITH 1;
```
