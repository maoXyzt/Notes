---
created: 2025-09-12T17:06:00.000+0800
modified: 2025-09-12T17:06:00.000+0800
---

# Sun-panel 个人导航面板部署

当内网部署的服务较多时，可以通过部署 sun-panel 导航页来整理这些服务的 URL，方便快速访问和管理。

本文通过 Docker Compose 方式部署 Sun-panel 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

> 参考文档: [在绿联NAS上部署个人导航页Sun-panel](https://support.ugnas.com/knowledgecenter/#/detail/eyJpZCI6MTQwNCwidHlwZSI6InRhZzAwMiIsImxhbmd1YWdlIjoiemgtQ04iLCJjbGllbnRUeXBlIjoiUEMiLCJhcnRpY2xlSW5mb0lkIjo0NzIsImFydGljbGVWZXJzaW9uIjoiMS4wIiwicGF0aENvZGUiOiIifQ==)

## 1 - 项目简介

Sun-panel 是一款轻量简洁的个人导航面板服务。

> [Sun-panel 官方文档](https://doc.sun-panel.top/zh_cn/)
> [Sun-panel 项目仓库](https://github.com/hslr-s/sun-panel)

> 2025-09-12: 开源最新版本为 1.3.0, 闭源最新版本为 1.7.0

## 2 - 使用 Docker Compose 部署 Sun-panel

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  sun-panel:
    image: hslr/sun-panel:latest
    container_name: sun-panel
    restart: unless-stopped
    volumes:
        - './database:/app/database'
        - './uploads:/app/uploads'
        - './conf:/app/conf'
    ports:
        - '3002:3002'
```

项目的挂载路径:

- `./database:/app/database`: 数据库文件存放在 `./database` 目录下
- `./uploads:/app/uploads`: 上传的文件保存路径
- `./conf:/app/conf`: 应用配置文件

项目的端口映射为本地的 3002 端口

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称：sun-panel
2. 存放路径(可自选): `共享文件夹/docker/sun-panel/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir sun-panel`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```

### 3 - 服务初始化

部署完成后，可通过 `http://<NAS_IP>:3002` 访问 sun-panel 的web界面。

初次登录需要用默认账户密码登录，默认账号为 `admin@sun.cc`，密码为 `12345678`

登录后建议新建一个账户密码，然后切换到新账户密码登录（注意：账户之间数据不互通）。

### 4 - 使用方法

在首页点击 “添加” 按钮，填写:

- 项目标题
- 描述信息
- 图标: 建议上传图标，防止在线图标加载失败
- 地址
- 内网地址
- 分组

点击 “保存” 即可在首页展示已添加的项目。

访问时，可以切换使用公网地址或内网地址访问。
