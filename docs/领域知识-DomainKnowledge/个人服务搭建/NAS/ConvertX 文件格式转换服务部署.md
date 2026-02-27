---
type: note
aliases: []
created: 2026-02-27T19:40:46.000+0800
modified: 2026-02-27T19:41:08.130+0800
---

本文通过 Docker Compose 方式部署 ConvertX 文件格式转换服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

## 1 - 项目简介

[ConvertX](https://github.com/C4illin/ConvertX) 是一款开源的文件格式转换工具，支持多种文件格式之间的转换。

## 2 - 使用 Docker Compose 部署 ConvertX

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  convertx:
    image: ghcr.io/c4illin/convertx
    container_name: convertx
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - JWT_SECRET=aLongAndSecretStringUsedToSignTheJSONWebToken1234 # will use randomUUID() if unset
      # - HTTP_ALLOWED=true # uncomment this if accessing it over a non-https connection
    volumes:
      - ./data:/app/data
```

项目的挂载路径:

- `./data:/app/data`: 数据存储路径

项目的端口映射为本地的 3000 端口。

项目的环境变量:

- `JWT_SECRET`: 可以用 `python3 -c "import secrets; print(secrets.token_hex(32))"` 生成一个随机字符串。
- `HTTP_ALLOWED`: 如果需要通过非 HTTPS 连接访问，请取消注释此行。

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称: convertx
2. 存放路径(可自选): `共享文件夹/docker/convertx/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir convertx`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```
