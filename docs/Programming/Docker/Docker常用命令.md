# docker 常用命令

## 1. 镜像

> [02、Docker常用命令 - 华为云 (huaweicloud.com)](https://www.huaweicloud.com/articles/1995d352dd7228cac90cd8737f1f5c97.html)

### 1.1 `pull` - 拉取或者更新镜像

```bash
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
```

```bash
# examples
docker pull python:3
docker pull registry.sensetime.com/zoetrope/python@sha256:c934af72b8bd03b9804d5bde2569c320926e70392d708d113a2e71bcf98c8a20
```

### 1.2 `images` - 列出镜像

```bash
docker images [OPTIONS] [REPOSITORY[:TAG]]
```

```bash
# examples
docker images			# 列出镜像，不含中间层
docker images ubuntu	# 列出REPOSITORY为ubuntu的镜像

# REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
# ubuntu              14.04               90d5884b1ee0        9 weeks ago         188 MB
# ubuntu              15.10               4e3b13c8a266        3 months ago        136.3 MB
```

### 1.3 `build` - 构建镜像

使用 `Dockerfile` 创建镜像

```bash
docker build [OPTIONS] PATH | URL | -
```

```bash
# examples
# 使用当前目录的 Dockerfile 创建镜像
docker build -t runoob/ubuntu:v1 .
# -t: 指定镜像标签

# 使用指定URL的 Dockerfile 创建镜像
docker build github.com/creack/docker-firefox

docker build -f /path/to/a/Dockerfile .
# -f: 指定 Dockerfile 文件的路径
```

### 1.4 `rmi` - 删除镜像

```bash
docker rmi [OPTIONS] IMAGE [IMAGE...]
```

```bash
docker rmi -f runoob/ubuntu:v4
# -f: 强制删除

docker rmi $(docker images -q)	# 删除所有镜像

# 删除无用镜像
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```

### 1.5 镜像发布流程

#### (1) `tag` - 标记镜像

增加镜像的repository和tag标记

```bash
docker tag [OPTIONS] IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]
```

```bash
# examples
docker tag ubuntu:15.10 runoob/ubuntu:v3
# REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
# runoob/ubuntu       v3                  4e3b13c8a266        3 months ago        136.3 MB

# 标记镜像到私有仓库
docker tag 95a6101eab8f registry.sensetime.com/zoetrope/python:3.8.10
```

#### (2) `login`/`logout` - 登录/登出镜像仓库

```bash
docker login [OPTIONS] [SERVER]
docker logout [OPTIONS] [SERVER]
```

```bash
# examples
docker login -u usrn -p pswd
docker login --username usrn --password pswd registry.sensetime.com

docker logout
docker logout registry.sensetime.com
```

#### (3) `push` - 上传镜像

需要登录到镜像仓库

```bash
docker push [OPTIONS] NAME[:TAG]
```

```bash
# examples
docker push registry.sensetime.com/zoetrope/python:3.8.10
```

### 1.6 `save`/`load` - 保存/加载镜像

保存：

```bash
docker save [OPTIONS] IMAGE [IMAGE...]
```

```bash
# examples
docker save runoob/ubuntu:v3 > my_ubuntu_v3.tar
docker save -o my_ubuntu_v3.tar runoob/ubuntu:v3
# -o: 输出到指定文件
```

加载：

```bash
docker load [OPTIONS]
```

```bash
# examples
docker load < busybox.tar.gz
docker load -i busybox.tar.gz
# -i: 指定导入文件，代替STDIN
```

## 2. 容器

### 2.1 `ps` - 列出容器

```bash
docker ps [OPTIONS]
```

```bash
# examples
docker ps		# 当前运行的容器
docker ps -a	# 所有容器，包括未运行的

# CONTAINER ID   IMAGE          COMMAND                ...  PORTS                    NAMES
# 09b93464c2f7   nginx:latest   "nginx -g 'daemon off" ...  80/tcp, 443/tcp          myrunoob
# 96f7f14e99ab   mysql:5.6      "docker-entrypoint.sh" ...  0.0.0.0:3306->3306/tcp   mymysql

docker ps -a -q # 列出所有创建的容器ID
# 09b93464c2f7
# b8573233d675
# b1a0703e41e7
# f46fb1dec520
```

### 2.2 `run` - 创建并运行容器

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

```bash
# examples
# 使用nginx:latest镜像创建容器
docker run --name mynginx -d nginx:latest
# -d: 以daemon方式启动
# --name：指定容器名称
docker run -p 8080:80 -v /test_data:/data -w /data -d nginx:latest
# -p: 映射容器80端口到宿主机8080端口
# -v: 映射宿主机/test_data目录到容器的/data目录(容器内自动创建)
# -w: 设置工作目录为/data；默认为/
docker run -it nginx:latest /bin/bash
# -it 以交互模式启动容器，在容器内开启/bin/bash （alpine类容器应使用/bin/sh）
```

> 相当于`docker create`之后再`docker start`该容器。

用`COMMAND`可以创建一个容器并用容器执行命令，命令完成后容器自动退出。

### 2.3 `exec` - 用容器执行命令

```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

```bash
# examples
docker exec -it mynginx /bin/sh /root/runoob.sh
# -it 以交互模式在容器内执行 /bin/sh /root/runoob.sh
```

### 2.4 `start`/`stop`/`restart` - 容器启动/停止/重启

```bash
docker start|stop|restart [OPTIONS] CONTAINER [CONTAINER...]
```

```bash
# examples
# 启动已被停止的容器；用容器名称指定
docker start myrunoob
# 停止运行中的容器；用容器ID指定
docker stop 09b93464c2f7
# 重启容器
docker restart myrunoob
```

### 2.5 `attach` - 进入容器

在`docker run`时使用`-d`参数，容器创建后会进入后台。此时想要进入容器，除了上面提到的 `docker exec -it xxxx /bin/bash` 外，还可以用`docker attach`（**不推荐**，退出时会导致容器停止）

```bash
docker attach [OPTIONS] CONTAINER
```

```bash
# examples
docker attach 09b93464c2f7
```

### 2.6 `rm` - 删除容器

```bash
docker rm [OPTIONS] CONTAINER [CONTAINER...]
```

```bash
# examples
docker rm -f db01 db02
# -f: 通过 SIGKILL 信号强制删除运行中的容器
docker rm -l db
# -l: 移除容器间的名为db的网络连接
docker rm -v nginx01
# -v: 删除容器并删除容器挂载的数据卷
docker rm $(docker ps -a -q)	# 删除所有已停止的容器
```

### 2.7 `export`/`import` - 导出/导入容器快照

导出：

```bash
docker export [OPTIONS] CONTAINER
```

```bash
# examples
# 导出本地容器
docker export 1e560fca3906 > ubuntu.tar
# 将容器按日期保存
docker export -o mysql-`date +%Y%m%d`.tar a404c6c174a2
# 保存为： mysql-20160711.tar
```

导入：

```bash
docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
```

```bash
# examples
# 从快照文件导入容器
cat docker/ubuntu.tar | docker import - test/ubuntu:v1
# 通过指定URL或目录来导入
docker import http://example.com/exampleimage.tgz example/imagerepo
```

### 2.8 其他查询功能

- `port`
- `logs`
- `top`
- `inspect`

```bash
# examples
# 查看容器的端口映射
dcoker port bf08b7f2cd89
# 5000/tcp -> 0.0.0.0:5000

# 查看容器内部的标准输出
docker logs -f bf08b7f2cd89
# -f: 跟踪日志（像`tail -f`一样输出）
docker logs --since="2016-07-01" --tail=10 mynginx
# --since: 显示某个开始时间的所有日志
# --tail: 只列出最新N条日志

# 查看容器内部运行的进程，
#   容器没有bash终端或top命令时也是可用的
docker top wizardly_chandrasekhar
# UID     PID         PPID          ...       TIME                CMD
# root    23245       23228         ...       00:00:00            python app.py

# 查看容器底层信息，
#    返回记录容器配置和状态信息的JSON
docker inspect wizardly_chandrasekhar
```

### 2.9 `kill` - kill容器

```bash
docker kill [OPTIONS] CONTAINER [CONTAINER...]
```

> 区别
>
> - `docker kill`: 默认向容器发送 **SIGKILL** 信号
> - `docker stop`: 向容器发送 **SIGTERM** 信号，等待一段时间未退出再发送 **SIGKILL** 信号

```bash
# examples
docker kill mynginx
docker kill -s KILL mynginx
# -s: 向容器发送一个指定信号

docker kill $(docker ps -a -q)	# 杀死所有正在运行的容器
```

### 2.10 `cp` - 容器与宿主机之间的数据拷贝

```shell
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH
```

无论容器是否正在运行都可以拷贝。容器内的路径可以省略开头的`/`。

```shell
# examples
# 宿主机向容器
docker cp foo.txt mycontainer:/foo.txt
# 容器向宿主机
docker cp mycontainer:/foo.txt foo.txt
# 目录拷贝
docker cp src/. mycontainer:/target
docker cp src/ mycontainer:/target
# ps: 旧版本docker进行目录拷贝时需要用`tar`和`-`
```

### 2.11 `commit` - 从容器创建镜像

```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
```

```bash
# examples
docker commit -a "runoob.com" -m "my apache" a404c6c174a2  mymysql:v1
# -a: 镜像作者
# -m: 提交时的文字说明
```

## 3. 清理

### 移除镜像

`docker image prune`：

```bash
# examples:
# 移除没有标签并且没有被容器引用的镜像（dangling镜像）
docker image prune
# 移除所有没有容器使用的镜像
docker image prune -a
# 跳过警告提示
docker image prune -f
# 过滤删除：超过24小时创建的镜像
docker image prune -a --filter "until=24h"
```

也可以用`docker rmi $(docker images --filter "dangling=true" -q --no-trunc)`删除所有dangling镜像


### 移除容器

一个停止的容器可写层仍然会占用磁盘空间。

`docker container prune`：

```bash
# examples
# ARGS: --filter, --force/-f
docker container prune
```

也可以用`docker rm $(docker ps -a -q)`删除所有已停止的容器。

### 移除卷

卷会被一个或多个容器使用，并且占用主机空间。卷不会自动移除，因为自动移除，会破坏数据。

`docker volume prune`：

```bash
# examples
# ARGS: --filter, --force/-f
docker volume prune
```

### 移除网络

Docker 网络不会占用磁盘空间，但是他们创建了 `iptables`规则，桥接网络服务，路由entries。

`docker network prune`：

```bash
# examples
# ARGS: --force/-f
docker network prune
```

### 移除Everything

`docker system prune`：用于移除镜像，容器，网络。

在 Docker 17.06.0 和更早，卷也是可以移除的。在Docker 17.06.1或更高版本，需要指定参数`--volumes`。

```bash
# examples
# ARGS: --all/-a, --filter, --force/-f, --volumes

docker system prune
# WARNING! This will remove:
#         - all stopped containers
#         - all networks not used by at least one container
#         - all dangling images
#         - all build cache
# Are you sure you want to continue? [y/N]

docker system prune --volumes
# WARNING! This will remove:
#         - all stopped containers
#         - all networks not used by at least one container
#         - all volumes not used by at least one container
#         - all dangling images
#         - all build cache
# Are you sure you want to continue? [y/N] y
```

### `rm`, `rmi`, `prune` 的差异

- `docker rm`：删除一个或多个 **容器**

- `docker rmi`：删除一个或多个 **镜像**

- `docker prune`：用来删除不再使用的 **docker 对象**

