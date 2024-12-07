# PostgresSQL 用户管理

用postgres账号登录psql

```bash
sudo -u postgres psql
```

查看所有用户名:

```
postgres=# \du
```

创建新用户

```sql
create user dev with password '******';
```

创建完成后，使用如下语句登录

```bash
psql -U dev -W
```

其他：

> 创建只读权限的用户：[PG数据库创建只读权限的用户](PG数据库创建只读权限的用户.md)
>
> 远程连接权限：[PG数据库允许远程连接](PG数据库允许远程连接.md)
