---
type: 
aliases: []
created: 2026-02-27T17:38:09.000+0800
modified: 2026-03-22T00:33:32.939+0800
---

## PG 断开所有连接

> [postgresql - How to drop all connections to a specific database without stopping the server? - Database Administrators Stack Exchange](https://dba.stackexchange.com/questions/16426/how-to-drop-all-connections-to-a-specific-database-without-stopping-the-server)

断开所有 `DB_NAME` 数据库的连接：

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
  AND datname='DB_NAME';
```

终止所有运行时间超过特定阈值的查询 (推荐做法):

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
  AND state = 'active'
  AND now() - query_start > interval '5 minutes';
```

仅终止包含 "SELECT" 关键字的活跃查询:

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
  AND state = 'active'
  AND upper(query) LIKE '%SELECT%';
```

终止特定用户的查询

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE usename = 'report_user'
  AND pid <> pg_backend_pid();
```
