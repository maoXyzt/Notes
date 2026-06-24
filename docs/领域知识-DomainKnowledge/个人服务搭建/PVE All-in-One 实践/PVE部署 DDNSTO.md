---
type: note
aliases: []
created: 2026-06-24T15:20:00.000+0800
modified: 2026-06-24T15:20:00.000+0800
---

## 0 - 简介

> 官网: <https://www.ddnsto.com/> ; 文档中心: <https://doc.linkease.com/zh/guide/ddnsto/>
> 本文 Linux 部署方式参考自官方文档: <https://www.koolcenter.com/t/topic/5868>

DDNSTO 是 koolcenter (易有云) 出品的一款内网穿透 / 远程访问工具。在**没有公网 IP** 的情况下，只要在内网任意一台设备上运行 DDNSTO 客户端，就能通过 `xxx.ddnsto.com` 的二级域名，从外网安全地访问内网中的各种 Web 服务 (NAS、路由器后台、HomeAssistant、各类自托管面板等)。

它和 [[PVE部署 Tailscale|Tailscale]] 解决的问题类似 (都是「在外面访问家里」)，但思路不同:

- **Tailscale** 组建的是点对点的虚拟局域网 (MesVPN)，访问端也需要安装客户端，访问的是原始内网 IP。
- **DDNSTO** 走的是「云端中转 + HTTP 反向代理」，访问端**无需安装任何客户端**，直接用浏览器打开分配的二级域名即可，适合把某个 Web 服务分享出去。

DDNSTO 本身不依赖 PVE，可以装在内网任意一台 Linux 机器上。本文介绍在 PVE 环境中的几种部署方式。

## 1 - 准备工作: 获取设备授权码 (令牌 Token)

无论用哪种方式安装，运行 DDNSTO 客户端时都需要一个**令牌 (Token)** 作为认证凭证。先把它拿到手:

1. 打开 [DDNSTO 控制台](https://www.ddnsto.com/)，点击右上角「控制台」，使用**微信扫码登录**。
2. 登录成功后，在用户中心 / 右上角处找到并复制你的「令牌 (Token)」。

令牌形如:

```plaintext
abcdefg-8888-8888-1111-abcdefghijk
```

> 这个令牌等同于你账号的设备授权凭证，请妥善保管，不要泄露。

## 2 - (推荐) 在 LXC 中安装

### 2.1 安装 Debian LXC

参考 [[PVE 安装 alpine LXC & Debian LXC]]，创建一个 Debian LXC。

安装参数参考:

- Container Type: Unprivileged
- 指定静态的 IPv4 IP 和 网关 IP (强烈建议分配静态 IP)
- Disk Size / RAM 给最小即可 (DDNSTO 客户端非常轻量，512 MiB 内存绰绰有余)

### 2.2 在 LXC 中安装 DDNSTO (一键脚本)

SSH (或在 PVE 中进入该 LXC 的 console) 后，执行如下一键安装脚本 (二选一):

```bash
sh -c "$(curl -sSL http://fw.koolcenter.com/binary/ddnsto/linux/install_ddnsto_linux.sh)"
```

或:

```bash
cd /tmp; wget --no-check-certificate http://fw.koolcenter.com/binary/ddnsto/linux/install_ddnsto_linux.sh; sh ./install_ddnsto_linux.sh
```

脚本运行过程中会**提示输入令牌 (Token)**，把第 1 节复制的令牌粘贴进去即可。脚本会自动下载对应架构 (amd64 / arm64) 的二进制，并注册为开机自启的后台服务。

### 2.3 验证安装

安装脚本完成后，DDNSTO 会以后台服务的形式运行。如果**成功连接服务器**，日志中会显示类似:

```plaintext
client init ok, username=xxxxx-xxxxxx-xxxxxx-xxx…
```

也可以回到 [DDNSTO 控制台](https://www.ddnsto.com/) 刷新页面，稍等片刻，设备会出现在设备列表中 (状态为在线)。

## 3 - 在 PVE host 中安装

如果不想单独开一个 LXC，也可以直接装在 PVE host 上 (PVE 底层是 Debian，glibc 发行版，兼容)。

SSH 到 PVE host，执行与上面相同的一键安装命令:

```bash
sh -c "$(curl -sSL http://fw.koolcenter.com/binary/ddnsto/linux/install_ddnsto_linux.sh)"
```

同样在提示时粘贴令牌即可。

> 一般不建议在 PVE host (宿主机) 上直接安装第三方服务，以保持宿主环境干净。这里仅作为一种可选方案列出，更推荐第 2 节的 LXC 方式或第 4 节的 Docker 方式。

### 3.1 手动安装 (可选)

如果一键脚本不可用，也可以手动下载二进制安装。从 [DDNSTO Linux 下载地址](https://fw.koolcenter.com/binary/ddnsto/linux/) 下载对应架构的文件:

- X86 平台: `ddnsto.amd64`
- ARM 平台 (树莓派等): `ddnsto.arm64`

以 X86 为例:

```bash
# 将下载好的二进制放到 /usr/local/bin/ddnsto
cp ddnsto.amd64 /usr/local/bin/ddnsto
chmod +x /usr/local/bin/ddnsto

# 以后台 (daemon) 方式启动，-u 后面替换为你的令牌
ddnsto -u abcdefg-8888-8888-1111-abcdefghijk -daemon
```

ARM 平台把 `ddnsto.amd64` 换成 `ddnsto.arm64` 即可。

## 4 - (替代方案) 使用 Docker 部署

> Docker 部署参考: <https://doc.linkease.com/zh/guide/ddnsto/install/device/docker.html>
> 镜像: [linkease/ddnsto](https://hub.docker.com/r/linkease/ddnsto/)

如果你已经有一台运行 Docker 的机器 (包括 Alpine LXC + Docker)，用官方镜像部署是最省心的方式，镜像自带运行环境，不受 glibc/musl 限制。

```bash
docker run -d \
  --name=ddnsto \
  --restart always \
  --network host \
  -e TOKEN=abcdefg-8888-8888-1111-abcdefghijk \
  -e DEVICE_IDX=0 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /your/config-path/ddnsto-config:/ddnsto-config \
  -e PUID=0 \
  -e PGID=0 \
  linkease/ddnsto
```

关键参数说明:

- `TOKEN`: 填写第 1 节从控制台拿到的令牌。
- `DEVICE_IDX`: 设备序号，默认 `0`；如果同一令牌下出现设备 ID 重复，改为 `1`~`100` 之间的值。
- `-v .../ddnsto-config:/ddnsto-config`: 持久化配置目录，保证容器重启后设备 ID 不变。**每个 DDNSTO 容器都应使用各自独立的配置目录路径。**
- `--network host`: 使用 host 网络，便于客户端访问到同网段的其他内网设备。

> 部分发行版执行 `docker` 命令需要加 `sudo` 前缀。

## 5 - 配置域名映射 (远程访问内网服务)

客户端跑起来、设备在控制台上线后，就可以为内网服务配置「域名映射」，从而通过二级域名远程访问。

1. 在 [DDNSTO 控制台](https://www.ddnsto.com/) 的设备列表中，找到刚上线的设备，点击「添加域名映射」的 `+` 按钮。
2. 填写映射配置:
    - **域名前缀**: 使用**小写字母或数字，且长度大于 6 个字符**。例如前缀 `kool666666`，对应访问地址 `https://kool666666.ddnsto.com`。
    - **目标主机**: 填内网服务的地址。80 端口可省略 (如 `http://192.168.50.1`)；非 80 端口必须写明 (如 `http://192.168.50.11:5000`)。
    - **协议**: 按目标服务选择 `http` 或 `https`。
3. 点击「添加」，**成功添加后约 1 分钟左右**即可正常访问。

之后在任意有网络的设备上，用浏览器打开 `https://你的前缀.ddnsto.com` 即可访问对应内网服务 (首次访问可能需要微信登录做身份验证)。

> 💡 多个内网服务可以各配一个前缀，互不影响。

## 6 - 常用管理命令

一键脚本方式安装后，DDNSTO 会注册为 systemd 服务，服务名为 `com.linkease.ddnstoshell`。

```bash
# 停止运行
systemctl stop com.linkease.ddnstoshell

# 启动
systemctl start com.linkease.ddnstoshell

# 查看运行状态
systemctl status com.linkease.ddnstoshell

# 设置 / 取消开机自启
systemctl enable com.linkease.ddnstoshell
systemctl disable com.linkease.ddnstoshell
```

Docker 方式的管理则用对应的 docker 命令:

```bash
docker stop ddnsto      # 停止
docker start ddnsto     # 启动
docker restart ddnsto   # 重启
docker logs -f ddnsto   # 查看日志 (确认 client init ok)
docker rm -f ddnsto     # 删除容器
docker pull linkease/ddnsto && docker rm -f ddnsto && <重新 run>   # 更新镜像
```
