# PVE 安装 Alpine LXC

+ PVE 系统版本: 8.3.0

LXC 是 Linux Container 的缩写，是 PVE 的一种轻量级的虚拟化技术。相比虚拟机，LXC 的性能更好，资源占用更少。

## 0 - 获取安装脚本

[Proxmox Community-Scripts](https://community-scripts.github.io/ProxmoxVE/) 提供了社区维护的安装脚本。

在其中可以找到安装 Alpine LXC 的脚本。

> <https://community-scripts.github.io/ProxmoxVE/scripts?id=alpine&category=Operating+Systems>
> 当前 (2025-11-03) 最新版本: alpine 3.22

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/alpine.sh)"
```

## 1 - 执行安装脚本

在 PVE 管理页面中，点击 pve node, 右侧面板中进入 shell。

执行上述脚本，按照提示完成安装。

### 1.1 安装过程中的选项

选择 "Advanced Settings" 选项进入安装设置。

+ "CONTAINER TYPE": 选择 "1 Unprivileged"
+ 输入两遍 root password
+ Container ID: 默认即可
+ "DISK SIZE": 默认 "1G", 改稍大一点 (例如, 20)
+ "CORE COUNT": CPU 核心数, 默认 "1", 改稍大一点 (例如, 2)
+ "RAM": 1024G
+ ... 一路默认即可
+ "SSH ACCESS": 选择 "YES", 允许 root 用户通过 SSH 访问
+ ... 一路默认即可
+ "Verbose Mode": 推荐开启，方便查看调试信息

最终我的安装配置如下:

```plaintext
    ___    __      _
   /   |  / /___  (_)___  ___
  / /| | / / __ \/ / __ \/ _ \
 / ___ |/ / /_/ / / / / /  __/
/_/  |_/_/ .___/_/_/ /_/\___/
        /_/
  🧩  Using Advanced Settings on node pve
  🖥️  Operating System: alpine
  🌟  Version: 3.22
  📦  Container Type: Unprivileged
  🔐  Root Password: ********
  🆔  Container ID: 103
  🏠  Hostname: alpine
  💾  Disk Size: 20 GB
  🧠  CPU Cores: 2
  🛠️  RAM Size: 1024 MiB
  🌉  Bridge: vmbr0
  📡  IPv4: DHCP
  📡  IPv6: SLAAC/AUTO
  ⚙️  Interface MTU Size: Default
  🔍  DNS Search Domain: Host
  📡  DNS Server IP Address: Host
  🏷️  Vlan: Default
  📡  Tags: community-script;os;alpine
  🔑  Root SSH Access: yes
  🗂️  Enable FUSE Support: no
  🔍  Verbose Mode: yes
  🚀  Creating a Alpine LXC using the above advanced settings
  💡  Writing configuration to /opt/community-scripts/alpine.conf
```

默认登录密码是 `alpine`。
