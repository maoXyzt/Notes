---
created: 2025-09-23T14:25:00.000+0800
modified: 2025-09-23T14:25:00.000+0800
---

# ezBookkeeping 自托管记账服务部署

本文通过 Docker Compose 方式部署 ezBookkeeping 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

## 1 - 项目简介

[ezBookkeeping](https://github.com/mayswind/ezbookkeeping) 是一款轻量级、自托管的个人财务APP。

其前端支持桌面浏览器和移动端浏览器访问，并支持PWA技术，可添加到桌面使用。

## 2 - 使用 Docker Compose 部署 IPTV-API

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  ezbookkeeping:
    image: mayswind/ezbookkeeping
    container_name: ezbookkeeping
    user: "1000:1000"
    ports:
      - "38080:8080"
    volumes:
      - ./data:/ezbookkeeping/data
      - ./log:/ezbookkeeping/log
      - ./storage:/ezbookkeeping/storage
    environment:
      - "EBK_GLOBAL_MODE=production"
      - "EBK_SERVER_DOMAIN=ezbookkeeping.yourdomain"
      - "EBK_SERVER_ENABLE_GZIP=true"
      - "EBK_LOG_MODE=file"
      - "EBK_SECURITY_SECRET_KEY=its_should_be_a_random_string"
```

项目的挂载路径:

- `./data:/ezbookkeeping/data`: 数据库文件存放在 `./data` 目录下 (sqlite3 数据库文件)
- `./log:/ezbookkeeping/log`: 日志文件存放在 `./log` 目录下
- `./storage:/ezbookkeeping/storage`: 默认对象存储使用本地文件系统, 根路径为 `./storage`

默认容器运行用户的 UID=1000, GID=1000, 建议检查确保挂载数据目录的权限。

项目的端口映射为本地的 18755 端口

配置选项说明:

可以用 `EBK_{SECTION_NAME}_{OPTION_NAME}` 形式通过环境变量设置。

默认的配置文件在 `/ezbookkeeping/config/ezbookkeeping.ini`, 可以参考默认配置文件的内容。

> 配置参考: [ezBookkeeping 配置文档](https://ezbookkeeping.mayswind.net/zh_Hans/configuration)。

secret_key 可以用 python 命令生成: `python -c "import secrets; print(secrets.token_hex(32))"`

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称：ezbookkeeping
2. 存放路径(可自选): `共享文件夹/docker/ezbookkeeping/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir ezbookkeeping`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```
