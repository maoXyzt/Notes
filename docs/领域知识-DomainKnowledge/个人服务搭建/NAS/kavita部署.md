---
created: 2025-10-29T20:49:00.000+0800
modified: 2025-10-29T20:49:00.000+0800
---

# Kavita 部署

Kavita 是一个自托管的媒体服务器，主要用于管理和阅读漫画、小说和电子书，支持多用户访问、跨设备同步以及多种文件格式。

本文通过 Docker Compose 方式部署 Kavita 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

> 参考文档: [在绿联NAS上搭建Kavita漫画管理工具](https://support.ugnas.com/knowledgecenter/#/detail/eyJpZCI6MTY3MywidHlwZSI6InRhZzAwMiIsImxhbmd1YWdlIjoiemgtQ04iLCJjbGllbnRUeXBlIjoiUEMiLCJhcnRpY2xlSW5mb0lkIjo1NDcsImFydGljbGVWZXJzaW9uIjoiMS4wIiwicGF0aENvZGUiOiIifQ==)

## 1 - 项目简介

Kavita 是一款开源的个人数字图书馆管理软件，支持多种电子书和漫画格式。

> [Kavita 项目仓库](https://github.com/Kareadita/Kavita)
> [Kavita 官方文档](https://wiki.kavitareader.com/)

主要特性：

1. 多格式支持：原生支持漫画（CBZ, CBR, ZIP, RAR）、电子书（EPUB, PDF, MOBI, AZW3）和小说（TXT, HTML, JSON），无需转换即可直接阅读。
2. 多用户系统：支持创建多个用户账号，可为不同用户分配独立的库、阅读权限和阅读进度，非常适合家庭或小团体共享。
3. 跨平台与响应式界面：提供网页端、移动端 App（iOS/Android）和桌面端应用，界面自适应各种设备，随时随地访问个人图书馆。
4. 智能元数据管理：自动从文件名或内嵌信息中提取书名、作者、封面等元数据，并支持手动编辑和在线刮削（如 AniList, MangaDex）来丰富书籍信息。
5. 阅读体验优化：提供多种阅读模式（如滚动、分页、双页）、自定义阅读方向（左到右、右到左）、夜间模式、书签和阅读进度同步等功能。
6. 内容组织灵活：支持创建书架、分类管理，并可通过标签、作者、系列等维度高效组织和查找内容。
7. 离线访问与同步：移动 App 支持下载内容离线阅读，阅读进度和书签可在所有设备间无缝同步。
8. 隐私与安全：作为自托管软件，所有数据存储在用户自己的服务器上，保障隐私安全；同时支持 HTTPS、双因素认证（2FA）等安全措施。
9. 持续更新与活跃社区：开源项目，开发活跃，功能迭代快，拥有积极的用户社区提供支持和插件。

## 2 - 使用 Docker Compose 部署 Kavita

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  kavita:
    image: jvmilazz0/kavita:latest    # Using the stable branch from the official dockerhub repo.
    container_name: kavita
    volumes:
      - ./manga:/manga
      - ./comics:/comics
      - ./books:/books
      - ./config:/kavita/config
    environment:
      - TZ=Asia/Shanghai
    ports:
      - "15000:5000"
    restart: unless-stopped
```

项目的挂载路径:

- `./config:/kavita/config`: 配置文件和数据存放在 `./config` 目录下
- `./manga:/manga`: 日式漫画(manga)文件存放路径（可选）
- `./books:/books`: 书籍文件存放路径（可选）
- `./comics:/comics`: 西式漫画(comics)文件存放路径（可选）

> 注意：您可以根据实际需要调整挂载的媒体目录。可以只挂载一个目录，也可以挂载多个不同类型的目录。

项目的端口映射为本地的 `15000` 端口

环境变量说明：

- `TZ=Asia/Shanghai`: 设置容器时区

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称: kavita
2. 存放路径(可自选): `共享文件夹/docker/kavita/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 "立即部署"

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir kavita`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 创建相应的挂载目录（如 `config`、`manga`、`books` 等）
5. 执行以下命令启动服务：

```bash
docker-compose up -d
```

## 3 - 服务初始化

部署完成后，可通过 `http://<NAS_IP>:15000` 访问 Kavita 的 Web 界面。

初次访问时，系统会引导您完成初始化设置：

1. 创建管理员账户：设置用户名、密码和邮箱
2. 配置媒体库：添加您的书籍或漫画目录
3. 设置扫描选项：配置自动扫描和元数据抓取选项

> 提示：建议在初始化后立即创建管理员账户，并配置好媒体库路径，以便 Kavita 能够自动扫描和索引您的文件。

## 4 - 配置建议

点击右上角齿轮图标，进入 "设置" 页面，可以进行以下配置：

### 4.1 语言设置

左侧 "Account" -> "Preferences", 右侧面板的 Global Settings 中, "Locale" 选择 "中文 (简体)"

### 4.2 Base Url

左侧 "服务" -> "常规", 右侧面板的 "路径" 中, 设置一个 Base Url, 以便配置到 nginx 代理的 location 中。
