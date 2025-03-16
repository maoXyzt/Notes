# Docker 配置镜像源(registry mirrors)

> 相关内容: [Docker 配置代理](./Docker配置代理.md)

在 Docker 的配置文件 `daemon.json` 中，`registry-mirrors` 的作用是指定 Docker 守护进程（daemon）使用的镜像仓库地址，以加快 Docker 镜像的下载速度。
通过配置 `registry-mirrors`，Docker 会优先使用配置的镜像地址进行镜像的拉取和推送操作。
如果配置的镜像地址上没有找到 Docker Hub 的镜像，Docker 会去官方的 Docker Hub 镜像仓库进行拉取。

简单来说，`registry-mirrors` 允许用户配置一个或多个镜像仓库作为 Docker Hub 的替代或补充，这些镜像仓库可以是位于本地或其他地区的，用于代替官方的 Docker Hub 镜像仓库。
这样做的好处是，可以减少因地理位置较远导致的网络延迟，提高镜像拉取的速度，尤其是在网络连接到 Docker Hub 速度较慢或不稳定的地区。

此外，配置 `registry-mirrors` 还可以帮助减少因大量 Docker 实例同时从互联网上拉取相同镜像而产生的额外流量。
在某些情况下，如果使用的镜像集合是明确且有限的，用户甚至可以手动拉取这些镜像并推送到一个简单的本地私有仓库中，从而完全依赖本地仓库而不是 Docker Hub。

Example:

`/etc/docker/daemon.json`

```json
{
    "registry-mirrors": [
        "https://docker.mirrors.ustc.edu.cn",
        "https://hub-mirror.c.163.com"
    ]
}
```

配置后，重启 docker 进程使配置生效。

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 额外说明

也可用 `chsrc` 命令来配置 `registry-mirrors`，如：

```bash
sudo chsrc set docker
# 或者 sudo chsrc set dockerhub
```

见 [Linux 开发环境 setup](../../Linux/Linux开发环境setup.md#全平台换源工具-chsrc)。
