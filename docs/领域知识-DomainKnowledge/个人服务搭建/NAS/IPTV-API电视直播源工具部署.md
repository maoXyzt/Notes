---
created: 2025-09-12T17:06:00.000+0800
modified: 2025-09-12T17:06:00.000+0800
---

# IPTV-API 电视直播源工具部署

IPTV-API 是一款超实用的 IPTV 电视直播源更新工具，可让您畅享不间断的精彩电视直播。它支持自定义频道，自动获取直播源接口，测速验效后生成可用的结果。

本文通过 Docker Compose 方式部署 IPTV-API 服务到绿联的 NAS 上。同时也提供了通用的部署方法，可供在其他 Linux 服务器上部署时参考。

> 参考文档: [在绿联 NAS 上部署IPTV电视直播源更新工具实现电视自由](https://support.ugnas.com/knowledgecenter/#/detail/eyJpZCI6MTUzMSwidHlwZSI6InRhZzAwMiIsImxhbmd1YWdlIjoiemgtQ04iLCJjbGllbnRUeXBlIjoiUEMiLCJhcnRpY2xlSW5mb0lkIjo1MzAsImFydGljbGVWZXJzaW9uIjoiMS4wIiwicGF0aENvZGUiOiIifQ==)

## 1 - 项目简介

> [IPTV-API 项目仓库](https://github.com/Guovin/iptv-api)

## 2 - 使用 Docker Compose 部署 IPTV-API

### 2.1 项目配置

编写 `docker-compose.yml` 的文件内容如下:

```yaml
services:
  iptv-api:
    image: guovern/iptv-api
    container_name: iptv-api
    ports:
      - "18755:8000"
    volumes:
      - ./config:/iptv-api/config
      - ./output:/iptv-api/output
```

项目的挂载路径:

- `./config:/iptv-api/config`: 配置文件存放在 `./config` 目录下
- `./output:/iptv-api/output`: 输出文件(数据和日志)存放在 `./output` 目录下

项目的端口映射为本地的 18755 端口

### 2.2 部署服务

#### (1) 通过 NAS UI 部署

进入 NAS 的管理界面，打开 Docker，在 "项目" 中点击 "创建"。

1. 项目名称：iptv-api
2. 存放路径(可自选): `共享文件夹/docker/iptv-api/`
3. Compose 配置: 将上述 `docker-compose.yml` 的内容导入或复制到此目录下
4. 启动项目: 点击 “立即部署”

#### (2) 在 Linux Server 上部署

如果是在服务器上部署，可以通过 SSH 登录到服务器:

1. 进入服务器，选择一个合适的目录存放项目文件，比如 `~/docker`
2. 创建项目目录 `mkdir iptv-api`
3. 在目录中创建 `docker-compose.yml` 文件，在其中写入上述配置内容
4. 执行以下命令启动服务：

```bash
docker-compose up -d
```

### 3 - 服务初始化

下面是不同地址对应的服务:

| 接口              | 描述          |
|:----------------|:------------|
| /               | 默认接口        |
| /m3u            | m3u 格式接口    |
| /txt            | txt 格式接口    |
| /ipv4           | ipv4 默认接口   |
| /ipv6           | ipv6 默认接口   |
| /ipv4/txt       | ipv4 txt接口  |
| /ipv6/txt       | ipv6 txt接口  |
| /ipv4/m3u       | ipv4 m3u接口  |
| /ipv6/m3u       | ipv6 m3u接口  |
| /content        | 接口文本内容      |
| /log/result     | 有效结果的日志     |
| /log/speed-test | 所有参与测速接口的日志 |

#### 3.1 订阅源配置

详细教程: <https://github.com/Guovin/iptv-api/blob/master/docs/tutorial.md>

服务启动后，打开浏览器访问 `http://<NAS_IP>:18755`，进入 IPTV-API 的登录页面。

#### 3.2 初始化源信息

首次访问可能会提示 "🔍️未找到结果文件，若已启动更新，请耐心等待更新完成..."。等待更新完毕（可在等待容器日志中出现 "Update completed" 字样）。

更新完毕后，再次访问 `http://<NAS_IP>:18755`，即可下载源信息。

### 4 - 使用方法

#### 4.1 接口地址

更新完毕后，再次访问 `http://<NAS_IP>:18755`，即可下载源信息。

#### 4.2 M3u 接口

在浏览器输入 `http://<NAS_IP>:18755/m3u`，下载 m3u 格式的源信息。

大部分 IPTV 项目都可以直接使用 m3u 地址。

比如在 IOS 上下载安装 Fileball 应用，免费版本允许设置一个 IPTV 源，我们选择“添加远程订阅”，然后填入我们自己 NAS 提供的 接口 URL 地址。

- Name: 自定义
- URL: `http://<NAS_IP>:8755/m3u` 请注意：外网访问需要使用公网IP地址。
- EPG: 一般为 `http://epg.51zmt.top:8000/e.xml`

配置完成后，点击存储的 IPTV 源，即可观看直播，实现电视自由。

#### 4.3 Txt 接口

影视仓请使用txt接口，不然会出现很多重复并且无用的频道。

在浏览器输入 `http://<NAS_IP>:18755/txt`，下载 txt 格式的源信息。

#### 4.4 接口内容

在浏览器输入 `http://<NAS_IP>:18755/content`，可以获取源信息。

#### 4.5 测速日志

在浏览器输入 `http://<NAS_IP>:18755/log`，可以获取不同频道的测速日志。

更多配置见: <https://github.com/Guovin/iptv-api/blob/master/docs/config.md>
