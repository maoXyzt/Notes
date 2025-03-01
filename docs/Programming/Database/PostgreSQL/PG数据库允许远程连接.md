# PG 数据库运行远程连接

PostgreSQL 安装后，默认只接受本地机器 (127.0.0.1) 连接访问。

要开启其他主机上访问 PostgreSQL 数据库的服务，需要配置 data 目录下的 `pg_hba.conf` 和 `postgresql.conf`。

默认路径参考（PG13）：

- `/etc/postgresql/13/main/pg_hba.conf`
- `/etc/postgresql/13/main/postgresql.conf`

## 1、pg_hba.conf 配置数据库的访问权限

找到 `# IPv4 local connections:` 后，添加一行参数：

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# IPv4 local connections:
host    all             all             0.0.0.0/0                trust
```

## 2. postgresql.conf 配置数据库服务响应地址范围

找到 `listen_addresses` 参数后，设置

```ini
listen_addresses = '*'
```

## 3. 重启服务

```bash
sudo systemctl restart postgresql
```
