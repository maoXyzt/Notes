# PostgreSQL 服务安装

## 1. 在系统上安装服务端

### 1.1 在 Ubuntu 系统上安装

<https://documentation.ubuntu.com/server/how-to/databases/install-postgresql/index.html>

```bash
sudo apt install postgresql
```

默认配置文件目录：`/etc/postgresql/<version>/main`

### 1.2 安装后开启远程访问

> 详见 [PG 数据库允许远程连接](./PG数据库允许远程连接.md)

配置 `/etc/postgresql/<version>/main/postgresql.conf`

```bash
listen_addresses = '*'
```

## 2. 用 docker

> 参考镜像的官方说明 <https://hub.docker.com/_/postgres>

Example:

```yml
# Config the following environment variables
# + DATABASE__PORT
# + DATABASE__USERNAME
# + DATABASE__PASSWORD
# + DATABASE__DB

services:
  postgres:
    image: postgres:16
    ports:
      - ${DATABASE__PORT-5432}:5432
    environment:
      POSTGRES_USER: ${DATABASE__USERNAME:-postgres}
      POSTGRES_PASSWORD: ${DATABASE__PASSWORD:-postgres}
      POSTGRES_DB: ${DATABASE__DB}
    volumes:
      - pg-data-volume:/var/lib/postgresql/data
    # set shared memory limit when using docker-compose
    shm_size: 128mb
    # or set shared memory limit when deploy via swarm stack
    healthcheck:
      test: [ "CMD", "pg_isready", "-U", "${DATABASE__USERNAME:-postgres}", "-d", "${DATABASE__DB}" ]
      interval: 5s
      retries: 5
    restart: always

volumes:
  pg-data-volume:
    name: postgres-data-volume
    driver: local
    driver_opts:
      type: none
      # path to mount PGDATA folder
      device: ./data/pgdata
      o: bind
```

## 3. 测试安装

### 用 psql 测试

安装依赖

```bash
sudo apt install postgresql-client
```

```bash
psql --host your-servers-dns-or-ip --username postgres --password --dbname template1
```

### 用 python 和 psycopg2 测试

安装依赖

```bash
pip install psycopg2
```

创建如下文件，并执行:

```python
import psycopg2

try:
    conn = psycopg2.connect(
        user = "postgres",
        password = "root",
        host = "127.0.0.1",
        port = "5432",
        database = "postgres",
    )

    cursor = conn.cursor()
    # Print PostgreSQL Connection properties
    print ( conn.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if('conn' in locals()):
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")
```
