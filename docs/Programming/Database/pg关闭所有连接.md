# PG 关闭所有连接

> [postgresql - How to drop all connections to a specific database without stopping the server? - Database Administrators Stack Exchange](https://dba.stackexchange.com/questions/16426/how-to-drop-all-connections-to-a-specific-database-without-stopping-the-server)

```sql
select pg_terminate_backend(pid) from pg_stat_activity where datname='DB_NAME';
```

