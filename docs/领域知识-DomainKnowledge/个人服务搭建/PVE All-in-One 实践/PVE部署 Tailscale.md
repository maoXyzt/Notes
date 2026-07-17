---
type: note
aliases: []
created: 2026-03-03T14:39:57.000+0800
modified: 2026-07-16T03:07:32.000+0800
---

## 1 - (推荐) 在 LXC 中安装

> 官方文档: [Tailscale in LXC containers](https://tailscale.com/docs/features/containers/lxc/lxc-unprivileged)

[Proxmox Community-Scripts](https://community-scripts.github.io/ProxmoxVE/) 提供了社区维护的安装脚本。

> <https://community-scripts.github.io/ProxmoxVE/scripts?id=add-tailscale-lxc>

该脚本是一个 addon，会在已存在的 LXC 容器中添加 tailscale。我们需要先安装一个 LXC。

### 1.1 安装 Alpine LXC

参考 [[PVE 安装 alpine LXC & Debian LXC]]，创建一个 Alpine LXC。

安装参数参考:

- Container Type: Unprivileged
- 指定静态的 IPv4 IP 和 网关 IP (强烈建议分配静态 IP)
- Enable TUN/TAP device support

```bash
  💡  PVE Version 8.3.0 (Kernel: 6.8.12-4-pve)
  🖥️  Operating System: alpine
  🌟  Version: 3.23
  📦  Container Type: Unprivileged
  🆔  Container ID: 103
  🏠  Hostname: alpine
  💾  Disk Size: 1 GB
  🧠  CPU Cores: 1
  🛠️  RAM Size: 512 MiB
  🌉  Bridge: vmbr0
  📡  IPv4: 192.168.50.21/24
  📡  IPv6: auto
  🗂️  FUSE Support: no
  📡  TUN/TAP Support: yes
  📦  Nesting: Enabled
  📦  Keyctl: Enabled
  🎮  GPU Passthrough: no
  📦  Protection: Enabled
  💡  Timezone: Asia/Shanghai
  🔍  Verbose Mode: yes
```

### 1.2 在 Alpine LXC 中安装 Tailscale

执行如下脚本:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/tools/addon/add-tailscale-lxc.sh)"
```

在交互式界面:

1. 选择 LXC (刚才安装的)

脚本自动完成安装。

ssh 到该 LXC，执行 `reboot` 命令。

重启后，在容器中执行 `tailscale up`:

```bash
alpine:~# tailscale up

To authenticate, visit:

        https://login.tailscale.com/a/xxxxxxxxxxxx
```

根据弹出的 URL，访问该地址，登录即可。

## 2 - 在 PVE host 中安装

> [Tailscale on a Proxmox host](https://tailscale.com/docs/integrations/proxmox)

在 PVE host 中安装方法类似于在普通 linux 机器中安装。

SSH 到 PVE host，执行如下安装命令:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

安装完成后，在容器中执行 `tailscale up`:

```bash
alpine:~# tailscale up

To authenticate, visit:

        https://login.tailscale.com/a/xxxxxxxxxxxx
```

根据弹出的 URL，访问该地址，登录即可。

## 3 - 开启子网路由 (subnet routing)

> 官方文档: [Subnet routers](https://tailscale.com/docs/features/subnet-routers)

通过将安装了 Tailscale 的机器设置为子网路由器，可以让外网设备直接通过原本的内网 IP 访问到内网的其他设备，而不需要给每台设备都安装 Tailscale。

### 3.1 第一步: 开启 Linux 系统的 IP 转发（IP Forwarding）

为了让这台机器能将 Tailscale 的网络流量转发到你家里的局域网，你需要开启系统的 IP 转发功能。

1) 如果 Linux 系统中有 `/etc/sysctl.d` 目录，在终端中依次运行以下命令:

```bash
# 开启 IPv4 和 IPv6 转发
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
# 让配置立即生效
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```

2) 否则，执行:

```bash
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf
```

3) 如果系统使用了 `firewalld`, 还需要允许 masquerading:

```bash
firewall-cmd --permanent --add-masquerade
```

### 3.2 第二步: 让 Tailscale 宣告内网网段

确认你家里的局域网网段（比如最常见的是 `192.168.1.0/24`）。

1) 使用带有 `--advertise-routes` 参数的命令重启 Tailscale（把下面的 IP 段替换为内网实际的网段。多个网段用逗号分隔）:

```bash
sudo tailscale up --advertise-routes=192.168.1.0/24
```

(如果需要其他启动参数，比如 `--advertise-exit-node`，一并加上)

2) 或者，用 `taslscale set` 命令更改配置

```bash
sudo tailscale set --advertise-routes=192.168.1.0/24,198.51.100.0/24
```

### 3.3 第三步：在 Tailscale 管理后台批准路由

处于安全考虑，你在机器上宣告了网段后，还需要去网页端后台手动批准：

- 登录 [Tailscale Admin Console (控制台)](https://login.tailscale.com/admin/machines)。
- 在 **Machines** 列表中找到你刚配置好的这台内网机器。
- 点击机器所在行最右侧的 **三个点 (...)**，选择 **Edit route settings**（编辑路由设置）。
- 在弹出的菜单中，找到 **Subnet routes**，勾选你刚刚宣告的网段（如 `192.168.1.0/24`），即可完成批准。

### 3.4 第四步：在外网设备上接受路由（Accept Routes）

你的外网设备（如手机、外出的笔记本电脑）需要配置为“接受子网路由”才能访问内网：

- **对于 Windows / macOS / iOS / Android 客户端**：  
	- 默认情况下，这些图形化客户端会自动接受子网路由。如果你发现连不上，可以点开客户端的设置菜单，确认 **"Use Tailscale subnets"**（使用 Tailscale 子网）这个选项处于**开启**状态。
- **对于 Linux 客户端**：  
		Linux 客户端默认不接受子网路由，你需要在这台外网机器上执行以下命令来启用：

```bash
sudo tailscale set --accept-routes
```

### 3.5 第五步: 验证子网可连接

可以在其他设备上 ping 子网路由设备的 "Tailscale IP" 地址。

"Tailscale IP" 可以在 admin console 中查看，在子网路由设备上执行 `tailscale ip -4` 命令查询。

## 4 - 其他功能

### 4.0 退出运行

```bash
tailscale down
```

### 4.1 Exit Node (出口节点)

如果你不仅想访问内网设备，还想让外网设备**所有的上网流量**都通过家里的宽带代理出去（比如为了看家里宽带专属的流媒体，或拥有家里的公网 IP），可以在启动时加上 `--advertise-exit-node` 参数，并在后台批准它作为 Exit Node。

### 4.2 自建 DERP 中继服务

详见 [[自建 Tailscale DERP 中继服务]]。
