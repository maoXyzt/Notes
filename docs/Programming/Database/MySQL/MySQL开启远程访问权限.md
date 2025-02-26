# MySQL开启远程访问权限

## 0. 检查防火墙状态

```bash
# 查看防火墙是否开启
systemctl status firewalld
# 检查端口是否开启
firewall-cmd --list-ports
```

## 1. 登录

```bash
mysql -u root -p
```

```sql
mysql> use mysql;
Database changed
mysql> select host, user from user;
+-----------+------------------+
| host      | user             |
+-----------+------------------+
| localhost | mysql.infoschema |
| localhost | mysql.session    |
| localhost | mysql.sys        |
| localhost | root             |
+-----------+------------------+
4 rows in set (0.00 sec)
```

可以看到，root账号的host为localhost

## 2. 实现远程连接（授权法）

将host字段的值改为%，表示可以在任何客户端机器上以root用户登陆。

```sql
mysql> update user set host = '%' where user = 'root';
```

将权限改为ALL PRIVILEGES

```sql
mysql> grant all privileges on *.* to root@'%' identified by "password";
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> select host,user,password from user;
+-----------+------------------+
| host      | user             |
+-----------+------------------+
| localhost | root             |
| localhost | mysql.infoschema |
| localhost | mysql.session    |
| localhost | mysql.sys        |
+-----------+------------------+
4 rows in set (0.00 sec)
```

## 3. (MySQL 8)修改加密规则

由于加密规则导致无法用桌面客户端远程连接

- MySQL8.0之前的版本密码加密规则：mysql_native_password
- MySQL8.0密码加密规则：caching_sha2_password

修改加密规则

```bash
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
```

修改后，可以查看密码root账号的密码加密规则已经修改

```sql
mysql> select host,user,plugin from user;
+-----------+------------------+-----------------------+
| host      | user             | plugin                |
+-----------+------------------+-----------------------+
| %         | root             | mysql_native_password |
| localhost | mysql.infoschema | caching_sha2_password |
| localhost | mysql.session    | caching_sha2_password |
| localhost | mysql.sys        | caching_sha2_password |
+-----------+------------------+-----------------------+
4 rows in set (0.00 sec)
```
