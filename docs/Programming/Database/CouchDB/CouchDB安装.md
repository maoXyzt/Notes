# CouchDB 安装

## 0. 安装前准备

- 服务器: 阿里云 ECS (Aliyun)
- OS: Ubuntu 22

## 1. 安装方式：Docker container

> <https://github.com/vrtmrz/obsidian-livesync/blob/main/docs/setup_own_server.md#a-using-docker-container>

1) Prepare

```bash
# Prepare directories which saving data and configurations.
mkdir couchdb-data
mkdir couchdb-etc
```

`docker-compose.yml`:

```yaml
version: "3"

services:
  couchdb:
    image: couchdb:3
    container_name: couchdb-3
    ports:
      - "5984:5984"
    volumes:
      - ./couchdb-data:/opt/couchdb/data
      - ./couchdb-etc:/opt/couchdb/etc/local.d
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: ${COUCHDB_PASSWORD}
    restart: always
```

## 2. 配置

关于 CouchDB 的配置文件

> 安装路径：`/opt/couchdb/`
>
> 配置文件 (相对于安装路径)：
>
> 1. `etc/default.ini`
> 2. `etc/default.d/*.ini`
> 3. `etc/local.ini`
> 4. `etc/local.d/*.ini`
>
> 升级或重安装时 `default.ini` 可能被覆盖，所以配置文件的修改应该在 `local.ini` 或 `local.d/*.ini` 中进行。
