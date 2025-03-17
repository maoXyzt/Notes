# PostgresSQL 用户管理

## 0. 登录 psql

用 `postgres` 账号登录 psql

```bash
sudo -u postgres psql
```

## 1. 查看所有用户

```bash
postgres=# \du
```

## 2. 创建新用户

创建新用户(用户名为 `dev`，密码为 `new_password`):

```sql
create user dev with password 'new_password';
```

创建完成后，使用如下语句登录

```bash
psql -U dev -W
```

其他：

> 创建只读权限的用户：[PG 数据库创建只读权限的用户](./PG数据库创建只读权限的用户.md)
>
> 远程连接权限：[PG 数据库允许远程连接](./PG数据库允许远程连接.md)
