# Syncthing 文件同步服务部署

本文通过 Docker Compose 方式部署 Syncthing 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

> 参考教程: [在绿联 NAS 上搭建 Syncthing 开源文件同步工具](https://support.ugnas.com/knowledgecenter/#/detail/eyJpZCI6MTA5NiwidHlwZSI6InRhZzAwMiIsImxhbmd1YWdlIjoiemgtQ04iLCJjbGllbnRUeXBlIjoiUEMiLCJhcnRpY2xlSW5mb0lkIjozNzIsImFydGljbGVWZXJzaW9uIjoiMS4wIn0=)

## 1 - 项目简介

[Syncthing](https://syncthing.net/) 是一款开源的文件同步工具，支持多平台客户端和浏览器插件，提供文件同步、备份等功能。

Syncthing 服务必须通过 https 访问，建议结合内网穿透、反向代理和 SSL 证书一起使用。

## 2 - 使用 Docker Compose 部署 Syncthing

> [Application Setup](https://docs.linuxserver.io/images/docker-syncthing/#application-setup)

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  syncthing:
    image: lscr.io/linuxserver/syncthing:latest   # 编写此文时，最新版本为 2.0.10
    container_name: syncthing
    volumes:
      - ./config:/config
      - /共享文件夹/syncthing-data:/data1
      #- /path/to/data2:/data2  # 如果要同步其他目录，可以添加 /data2 的映射
    ports:
      - 38384:8384
      - 32000:22000
      - 32000:22000/udp
      - 31027:21027/udp
    environment:
      PUID: 1000
      PGID: 10
      TZ: Asia/Shanghai
    restart: unless-stopped
```

项目的挂载路径:

- `./config:/config`: 配置文件存放在 `./config` 目录下
- `/共享文件夹/syncthing-data:/data1`: 同步的数据文件目录。如果要同步其他目录，可以修改为其他路径。

项目的端口映射:

(如果 NAS 上已经运行了其他程序占用了 22000 或 8395 端口，例如使用 Pro 系统同步与备份功能，建议选择其他未被占用的端口)

- `38384:8384`: Syncthing Web UI (TCP)
- `32000:22000`: Syncthing sync (TCP)
- `32000:22000/udp`: Syncthing sync (UDP, optional for QUIC)
- `31027:21027/udp`: Syncthing discovery (UDP)

环境变量配置:

- `PUID=1000`: 运行的用户 ID，根据实际用户 ID 设置
- `PGID=1000`: 运行的用户组 ID，根据实际用户组 ID 设置
- `TZ=Asia/Shanghai`: (可选) 时区设置

### 2.2 部署服务

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称：syncthing
2. 存放路径: `共享文件夹/docker/syncthing`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此处
4. 启动项目: 点击 “立即部署”

![创建项目](./.assets/wallos-NAS-创建项目.png)

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 创建项目目录 `mkdir syncthing`
2. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
3. 执行以下命令启动服务：

```bash
docker-compose up -d
```

## 3 - 服务初始化

部署完成后，可通过 `http://<NAS_IP>:8384` 访问 syncthing 的 web 界面。

点击【设置 ＞ 图形用户界面】，在页面中设置图形管理界面的用户名和密码。如果需要，还可以修改设备名方便辨认，点击“保存”生效。

默认的文件夹模板可以删除，进入文件夹选项点击“移除”。

## 4 - 使用方法

### 4.1 添加文件同步的共享设备

为了使用 syncthing 进行文件同步，我们需要到 syncthing 官网下载对应系统环境的软件进行备份设置。

这里以 Win 系统下使用 syncthing 软件举例说明，其他系统请参考 syncthing 官方文件。

1. 安装完成后，打开软件，会自动打开浏览器访问 `http://127.0.0.1:8384`。

2. 点击右上角的【操作＞显示 ID】按钮，会显示设备的 ID。复制这个ID，这个是本机电脑的设备 syncthing ID。

3. 打开 NAS 的容器 web 页面，在页面中点击“添加远程设备”，粘贴刚才复制的 syncthing ID，点击“保存”生效。

4. 回到win系统上运行的syncthing web，可以看到此时多了一个新设备的添加请求，点击“添加设备”，随后在添加窗口点击“保存”生效。两边互相添加设备后就可以连接上了。
