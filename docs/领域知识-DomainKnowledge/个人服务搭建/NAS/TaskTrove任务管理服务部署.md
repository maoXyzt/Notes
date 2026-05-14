---
type: note
aliases: []
created: 2026-05-08T17:01:23.000+0800
modified: 2026-05-09T00:00:00.000+0800
---

# TaskTrove 任务管理服务部署

TaskTrove 是一款自托管的任务管理服务，可以用来替代 Todoist、TickTick 等在线任务管理工具，将任务数据完全保留在本地。

本文通过 Docker Compose 方式部署 TaskTrove 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

## 1 - 项目简介

TaskTrove 是一款开源、自托管的任务管理面板服务，支持项目分组、标签、子任务、提醒等常见的任务管理功能。

> [TaskTrove 项目仓库](https://github.com/dohsimpson/tasktrove)

## 2 - 使用 Docker Compose 部署 TaskTrove

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  tasktrove:
    image: ghcr.io/dohsimpson/tasktrove:latest
    container_name: tasktrove
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
    # environment:
    #   - AUTH_SECRET=CHANGE_ME
```

项目的挂载路径:

- `./data:/app/data`: 数据库及任务数据存放在 `./data` 目录下

项目的端口映射为本地的 3000 端口。

如需启用认证功能，可取消 `environment` 部分的注释，将 `AUTH_SECRET` 设置为一个随机字符串。

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称: tasktrove
2. 存放路径(可自选): `共享文件夹/docker/tasktrove/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 "立即部署"

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir tasktrove`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```

### 3 - 服务初始化

部署完成后，可通过 `http://<NAS_IP>:3000` 访问 TaskTrove 的 web 界面。

首次访问需要根据页面提示创建管理员账户，设置用户名和密码后即可登录使用。

### 4 - 使用方法

登录后，可在主界面进行任务管理：

- 创建项目: 在左侧导航栏点击 "添加项目"，对任务进行分组管理
- 添加任务: 在项目中点击 "添加任务"，填写任务标题、描述、截止日期、优先级等信息
- 标签: 为任务添加标签，便于分类和筛选
- 子任务: 在任务详情中创建子任务，拆分复杂任务
- 筛选与搜索: 通过侧边栏的 "今天"、"即将到来" 等视图，或使用搜索功能快速定位任务

数据均保存在挂载的 `./data` 目录中，建议定期备份该目录以防数据丢失。
