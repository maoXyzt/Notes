# Nginx Proxy Manager 服务部署

本文通过 Docker Compose 方式部署 Nginx Proxy Manager 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

## 1 - 项目简介

> 项目主页: <https://nginxproxymanager.com/>

Nginx Proxy Manager 是一个开源的反向代理工具，支持通过 Web 界面管理 Nginx 配置。

## 2 - 部署方法

> 官方文档: <https://nginxproxymanager.com/guide/#quick-setup>

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    container_name: nginx-proxy-manager
    restart: unless-stopped
    environment:
      INITIAL_ADMIN_EMAIL: my@example.com
      INITIAL_ADMIN_PASSWORD: mypassword1
    ports:
      - '31080:80'
      - '31081:81'
      - '31443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```

项目的挂载路径:

- `./data:/data`: 挂载数据目录
- `./letsencrypt:/etc/letsencrypt`: 挂载证书目录

项目的端口映射:

- `31080:80`: 服务的 80 端口映射到本地的 31080 端口, 用于 http 访问
- `31081:81`: 服务的 81 端口映射到本地的 31081 端口, 用于管理界面的访问
- `31443:443`: 服务的 443 端口映射到本地的 31443 端口, 用于 https 访问

项目的环境变量:

- `INITIAL_ADMIN_EMAIL`: 初始管理员邮箱。如未提供, 默认为 `admin@example.com`
- `INITIAL_ADMIN_PASSWORD`: 初始管理员密码。如未提供, 默认为 `changeme`

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称：nginx-proxy-manager
2. 存放路径(可自选): `共享文件夹/docker/nginx-proxy-manager/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

![创建项目](./.assets/nginx-proxy-manager-NAS-创建项目.png)

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir nginx-proxy-manager`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```

### 3 - 服务初始化

部署完成后，打开浏览器访问 `http://<NAS-IP>:30081`，即可看到 Nginx Proxy Manager 的 Web 界面。

默认 Admin User 为:

```plaintext
Email:    admin@example.com
Password: changeme
```

如果通过环境变量 `INITIAL_ADMIN_EMAIL` 和 `INITIAL_ADMIN_PASSWORD` 设置了初始管理员邮箱和密码，则使用设置的邮箱和密码登录。

登录后会提示修改密码，修改密码后即可正常使用。
