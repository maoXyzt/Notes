---
created: 2025-09-15T11:54:00.000+0800
modified: 2025-09-15T11:54:00.000+0800
---

# Vaultwarden 个人密码管理服务部署

本文通过 Docker Compose 方式部署 Vaultwarden 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

## 1 - 项目简介

[Bitwarden](https://bitwarden.com/) 是一款开源的密码管理服务，支持多平台客户端和浏览器插件，提供密码生成、存储、自动填充等功能。

Vaultwarden (前称 Bitwarden_RS) 是 Bitwarden 服务端的一款轻量级开源替代品，与官方的 Bitwarden 客户端兼容。它可以自托管，支持 Docker 部署，易于安装和维护。

> [Vaultwarden 项目仓库](https://github.com/dani-garcia/vaultwardeno)

vaultwarden 服务必须通过 https 访问，建议结合内网穿透、反向代理和 SSL 证书一起使用。

## 2 - 使用 Docker Compose 部署 Vaultwarden

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    environment:
      # DOMAIN: "https://vaultwarden.example.com"
      SIGNUPS_ALLOWED: "true"
    volumes:
      - './vw-data:/data'
    ports:
      - '8000:80'
```

环境变量说明:

- `DOMAIN`: 当通过反向代理访问时需要设置，指定你的域名，确保 vaultwarden 知道使用 https 来正确处理附件等功能
- `SIGNUPS_ALLOWED`: 是否允许注册新用户，建议在创建好管理员账号后设置为 `false` 并重启服务，以防止陌生人注册

项目的挂载路径:

- `./vw-data:/data`: 保存的用户数据存放在 `./vw-data` 目录下

> ! 由于用户密码数据比较重要，建议对存储目录进行定期备份。

项目的端口映射为本地的 8000 端口

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称: vaultwarden
2. 存放路径(可自选): `共享文件夹/docker/vaultwarden/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir vaultwarden`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```

### 3 - 服务初始化

服务启动后，打开浏览器访问 `http://<NAS_IP>:18000`，进入 vaultwarden 的登录页面。

#### 3.1 创建账户

点击【创建账户】按钮，进入注册页面。

![vaultwarden 登录/注册页面](./.assets/vaultwarden-register.png)

依次输入邮箱、名称（可选）、新主密码、确认新主密码，点击【创建账户】按钮，完成注册。

注册完成后，会自动登录。

#### 3.2 配置网址

如果有公网 IP，可以结合反向代理、DDNS 等方案，将 vaultwarden 的访问地址映射到公网。

如果没有公网 IP，可以结合 DDNSTO、节点小宝、花生壳等 内网穿透服务，将 vaultwarden 的访问地址映射到公网。

配置完成后，在 vaultwarden 的项目配置中，environment 中添加 `DOMAIN` 变量，值为映射后的服务域名，并重启服务。

#### 3.3 关闭注册

在 vaultwarden 的项目配置中，environment 中添加 `SIGNUPS_ALLOWED` 变量，值为 `false`，并重启服务。

### 4 - 使用方法

#### 4.1 导入数据

如果之前已经有 bitwarden 的账号数据，可以导入到 vaultwarden 中。

在 bitwarden 的 “工具 -> 导出密码库” 中，选择文件格式（建议加密），点击【确认格式】进行导出。

![bitwarden 导出数据](./.assets/bitwarden-export.png)

在 vaultwarden 的 “工具 -> 导入数据” 中，选择文件格式和文件，点击【导入数据】按钮。

![vaultwarden 导入数据](./.assets/vaultwarden-import.png)
