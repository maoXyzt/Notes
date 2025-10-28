---
created: 2025-10-27T22:10:00.000+0800
modified: 2025-10-27T22:10:00.000+0800
---

# RustFS 部署

## 1 - 项目简介

[RustFS](https://github.com/rustfs/rustfs) 是一个基于 Rust 语言编写的 S3 兼容的文件系统。

其功能类似 MinIO，但运行时的资源占用更低，且提供了友好的 Web UI。

编写本文时，RustFS 项目目前仍处于 alpha 阶段 (最新版本 1.0.0-alpha.65)，尚未稳定，仅供参考。

> 2025-10-27: 最新版本为 1.0.0-alpha.65

## 2 - 使用 Docker Compose 部署 RustFS

### 2.1 项目配置

官方提供了 `docker-compose.yml` 的示例文件，文件内容见 <https://github.com/rustfs/rustfs/blob/main/docker-compose.yml>。

我们本次部署主要除了 rustfs 服务外还用到了 observability 相关服务，其他服务 (dev, cache, proxy) 暂时不需要，可以从 `docker-compose.yml` 中删除。

下载官方的代码 zip 包，解压后只保留 `.docker/` 目录和 `deploy/` 目录，以及 `docker-compose.yml` 文件。

修改 `docker-compose.yml` 删除不需要的内容，如 dev, cache, proxy 相关服务，多余的 volumes 声明。

经过精简后的 `docker-compose.yml` 文件内容如下:

```yaml
version: "3.8"

services:
  # RustFS main service
  rustfs:
    security_opt:
      - "no-new-privileges:true"
    image: rustfs/rustfs:latest
    container_name: rustfs-server
    ports:
      - "9000:9000" # S3 API port
      - "9001:9001" # Console port
    environment:
      # - RUSTFS_VOLUMES=/data/rustfs{0...3}  # Define 4 storage volumes
      - RUSTFS_ADDRESS=0.0.0.0:9000
      - RUSTFS_CONSOLE_ADDRESS=0.0.0.0:9001
      - RUSTFS_CONSOLE_ENABLE=true
      - RUSTFS_EXTERNAL_ADDRESS=:9000  # Same as internal since no port mapping
      - RUSTFS_CORS_ALLOWED_ORIGINS=*
      - RUSTFS_CONSOLE_CORS_ALLOWED_ORIGINS=*
      - RUSTFS_ACCESS_KEY=rustfsadmin
      - RUSTFS_SECRET_KEY=rustfsadmin
      - RUSTFS_LOG_LEVEL=info
      - RUSTFS_TLS_PATH=/opt/tls
    volumes:
      - ./deploy/data/pro:/data
      - ./deploy/logs:/app/logs
      - ./deploy/data/certs/:/opt/tls # TLS configuration, you should create tls directory and put your tls files in it and then specify the path here
    networks:
      - rustfs-network
    restart: unless-stopped
    healthcheck:
      test:
        [
          "CMD",
          "sh", "-c",
          "curl -f http://localhost:9000/health && curl -f http://localhost:9001/health"
        ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  rustfs-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

项目挂载路径:

- `deploy/data/pro:/data`: 数据存储路径
- `deploy/logs:/app/logs`: 日志存储路径
- `deploy/data/certs/:/opt/tls`: TLS 证书存储路径

项目的端口映射:

- `9000:9000`: S3 API 端口
- `9001:9001`: Console 端口

环境变量:

- `RUSTFS_ACCESS_KEY=rustfsadmin`: 访问密钥，建议修改为随机字符串
- `RUSTFS_SECRET_KEY=rustfsadmin`: 秘密密钥，建议修改为随机字符串

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称: rustfs
2. 存放路径(可自选): `共享文件夹/docker/rustfs/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir rustfs`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```
