---
type: note
aliases: []
created: 2026-11-18T00:18:17.000+0800
modified: 2026-11-18T00:39:26.857+0800
---

Nginx Proxy Manager（简称 NPM）提供 Web 管理界面，用于配置反向代理、域名转发和 HTTPS 证书，适合作为家庭自托管服务的统一入口。

本文使用 Proxmox Community Scripts 在 PVE 上创建独立的 LXC 容器并安装 NPM。操作方式参考 [[PVE 安装 alpine LXC & Debian LXC]]。

> 本文于 2026-11-18 核对上游脚本，尚未在本机 PVE 实测。脚本随上游更新，实际参数和提示以执行时为准；参考笔记中的 PVE 8.3.0 不代表本文已验证兼容的版本。

## 1 - 安装 Nginx Proxy Manager LXC

### 1.1 安装脚本

> [Community Scripts：Nginx Proxy Manager](https://community-scripts.org/scripts?q=nginx&preview=nginxproxymanager)
>
> 当前脚本默认：Debian 13、非特权容器、2 核 CPU、2048 MiB 内存、8 GB 磁盘。NPM 版本在安装时获取上游最新 release。

在 PVE 管理页面中，选择 pve node，进入右侧的 **Shell**，以 root 执行：

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/nginxproxymanager.sh)"
```

脚本会创建 LXC 并安装应用，无需提前手动创建 Debian 容器。该方案在 LXC 中直接运行 NPM 和 OpenResty，使用 systemd 管理服务，不需要另外安装 Docker。

脚本来源：[LXC 创建与更新脚本](https://github.com/community-scripts/ProxmoxVE/blob/main/ct/nginxproxymanager.sh)、[容器内安装脚本](https://github.com/community-scripts/ProxmoxVE/blob/main/install/nginxproxymanager-install.sh)。上述命令会下载并执行远程代码，执行前可通过这两个链接查看内容。

### 1.2 安装过程中的选项

采用 Default Settings 即可:

```plaintext
⚙️  Using Default Settings on node pve
  💡  PVE Version 8.3.0 (Kernel: 6.8.12-4-pve)
  🆔  Container ID: 104
  🖥️  Operating System: debian (13)
  📦  Container Type: Unprivileged
  💾  Disk Size: 8 GB
  🧠  CPU Cores: 2
  🛠️  RAM Size: 2048 MiB
  🚀  Creating a Nginx Proxy Manager LXC using the above default settings
```

NPM 作为代理入口需要稳定的 IP。若选择静态地址，应填写带前缀长度的地址，例如 `192.168.1.10/24`，并避开 DHCP 动态分配范围。

安装期间会下载依赖、编译 OpenResty 和构建前端。等待脚本提示完成后，记录容器 ID、IP 和实际安装的 NPM 版本。这里不预填安装结果。

## 2 - 首次访问

在局域网浏览器访问：

```text
http://<LXC-IP>:81
```

注意填写 **LXC 的 IP**，不是 PVE 宿主机的 IP。首次启动可能需要等待数据库初始化。

当前上游代码在未预设管理员环境变量时使用首次设置向导，按页面提示创建管理员账号；容器的 root 密码与 NPM 管理账号是两套凭据。不要直接套用旧教程中的默认账号密码。参见 [NPM 初始化代码](https://github.com/NginxProxyManager/nginx-proxy-manager/blob/master/backend/setup.js)。

端口用途如下，见 [NPM 官方安装说明](https://nginxproxymanager.com/setup/)：

| TCP 端口 | 用途 | 访问范围建议 |
| --- | --- | --- |
| 80 | HTTP 代理入口 | 按业务需要开放 |
| 443 | HTTPS 代理入口 | 按业务需要开放 |
| 81 | NPM 管理页面 | 仅内网或 VPN |

若启用了 PVE、容器或路由器防火墙，需要放行相应流量；同时保证 NPM 能访问后端服务的实际端口。

## 3 - 添加反向代理

以下地址仅为示例，使用时替换为自己的域名和 IP：

```text
浏览器 → app.example.com → NPM（192.168.1.10）→ 后端服务（192.168.1.20:3000）
```

### 3.1 配置域名解析

只在内网访问时，在内网 DNS 中将 `app.example.com` 解析到 NPM 的内网 IP。也可以先通过客户端 hosts 文件测试。

需要公网访问时，将域名解析到家庭公网地址，并将路由器的 TCP 80、443 转发到 NPM 容器对应端口。动态公网 IP 还需要 DDNS。公网入口部署方式可参考 [NPM 官方指南](https://nginxproxymanager.com/guide/)。

### 3.2 添加 Proxy Host

进入 **Hosts → Proxy Hosts → Add Proxy Host**，填写：

| 字段 | 示例 |
| --- | --- |
| Domain Names | app.example.com |
| Scheme | http（按后端实际协议选择） |
| Forward Hostname / IP | 192.168.1.20 |
| Forward Port | 3000 |
| Websockets Support | 后端需要 WebSocket 时开启 |

保存后访问 `http://app.example.com`，确认能打开后端服务。

`Forward Hostname / IP` 应填写 NPM 容器能访问的后端地址。`127.0.0.1` 指向 NPM 容器自身，仅适用于后端也运行在该容器内的情况。

### 3.3 配置 HTTPS

确认 HTTP 转发正常后，在 Proxy Host 的 **SSL** 页面选择已有证书，或申请 Let's Encrypt 证书。证书生效并验证 HTTPS 正常后，再开启 **Force SSL**。

也可以先在 **SSL Certificates** 中添加自有证书，再关联到 Proxy Host。NPM 支持 Let's Encrypt 和自定义证书，详见 [官方功能说明](https://nginxproxymanager.com/guide/)。

## 4 - 检查与维护

### 4.1 服务状态和日志

在 **NPM 容器的 Console** 中执行：

```bash
systemctl status npm openresty --no-pager
journalctl -u npm -u openresty -n 100 --no-pager
ss -lntp
```

当前社区脚本创建的服务名为 `npm` 和 `openresty`，见前文容器内安装脚本。

+ 管理页面打不开：检查容器 IP、81 端口监听、服务状态和防火墙。
+ 代理返回 502：检查后端地址、端口、协议，以及容器到后端的网络连通性。
+ 域名无法访问：确认客户端解析到预期入口；公网访问还需要检查路由转发。
+ 安装卡在下载或构建：根据 Verbose 输出检查 DNS、外网连接、内存和磁盘空间。

### 4.2 更新与备份

更新前先通过 PVE 对整个 LXC 做备份。若需要单独备份应用数据，应包含 `/data` 和 `/etc/letsencrypt`；复制 SQLite 数据库时应先停止应用或使用一致性备份方式。更新可能中断代理服务，安排在可接受的维护时间进行。

在 **已安装 NPM 的容器 Console** 中重新执行社区脚本，进入其更新流程：

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/nginxproxymanager.sh)"
```

首次创建在 **PVE 节点 Shell** 执行，后续更新在 **NPM 容器内** 执行。更新完成后重新检查管理页面、已有代理域名和 HTTPS 证书。
