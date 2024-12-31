# Obsidian 同步 - 配置 LiveSync 与自托管 CouchDB 服务器

> [obsidian-livesync/docs/setup_own_server.md](https://github.com/vrtmrz/obsidian-livesync/blob/main/docs/setup_own_server.md#2-run-couchdb-initsh-for-initialise)

本文介绍了如何使用 Docker 和自托管 CouchDB 服务器配置 Obsidian LiveSync 同步。步骤包括安装 Docker 和 CouchDB 服务端，配置环境变量和服务端口，以及通过 Self-hosted LiveSync 插件在 Obsidian 客户端进行设置。最终实现 Obsidian 笔记的实时同步。

## 0. 安装依赖

### 0.1 安装 Docker

> [安装 Docker 并使用_云服务器 ECS(ECS)-阿里云帮助中心](https://help.aliyun.com/zh/ecs/use-cases/deploy-and-use-docker-on-alibaba-cloud-linux-2-instances?spm=5176.22414175.sslink.1.775b33actyjx4g)

```bash
yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine
yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
yum-config-manager \
    --add-repo \
    https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
```

## 1. 安装 CouchDB 服务端

使用利用下述工程的 `docker-compose.yml` 文件，启动 CouchDB 服务端。

> [vrtmrz/self-hosted-livesync-server](https://github.com/vrtmrz/self-hosted-livesync-server/tree/main)

### 1.1 获取源码

```bash
git clone --depth=1 https://github.com/vrtmrz/self-hosted-livesync-server.git
```

### 1.2 修改服务配置

配置环境变量(创建 `.env` 文件)

```properties
COUCHDB_SERVER=localhost:5984
COUCHDB_USER=admin
COUCHDB_PW=password
```

修改 `docker-compose.yml` 和 `config/init.ini` 文件中的 `e=_`:

```bash
sed -i 's/e=_/your-secret-words/' docker-compose.yml
sed -i 's/e=_/your-secret-words/' config/init.ini
```

CouchDB 将可通过该 URI 访问: `https://server-hostname.com/your-secret-words`

### 1.3 启动服务

```bash
docker network create caddy
docker compose up -d
```

访问 `http://server-hostname.com/your-secret-words` 或 `http://server-hostname.com:5984`，输入用户名和密码登录。

### 1.4 CouchDB 初始化配置

```bash
# Parameters used to connect to the CouchDB server.
export hostname=localhost:5984
export username=admin
export password=password

curl -s https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/utils/couchdb/couchdb-init.sh | bash
```

## 2. 暴露服务端口

通过服务器控制台，配置安全组规则，开放 5984 端口。

## 3. 配置客户端

### 3.1 生成 Setup URI

在服务端或者客户端执行以下命令，获取配置信息:

```bash
# Prepare environment variables.
# export hostname = https://server-hostname.com/your-secret-words
export hostname=http://server-hostname.com:5984
export admin=admin
export password=password
export database=obsidiannotes
export passphrase=dfsapkdjaskdjasdas

deno run -A https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/main/utils/flyio/generate_setupuri.ts
```

复制输出的 Setup URI： `obsidian://setuplivesync?settings=...`

### 3.2 通过 Self-hosted LiveSync 插件的 Setup Wizard 配置

打开 Obsidian 的 Self-hosted LiveSync 插件配置：

1. 在 Setup Wizard 中点击 `Use`，粘贴 Setup URI
2. 输入 `welcome`
3. 选择 `yes` & `Set it up as ...` (如果是第一次同步，要用本地文件覆盖远端，则选择第二个选项)
4. 选择 `Keep them disabled`
5. 重启 app
