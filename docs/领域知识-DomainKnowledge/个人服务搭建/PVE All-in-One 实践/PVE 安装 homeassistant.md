# PVE 安装 homeassistant

基于 PVE 8.3.0

## 0. 登录 PVE 的管理页面

`https://<IP>:8006`

## 1. 创建虚拟机

配置要点如下：

```ini
[一般]
名称="HA"
[操作系统]
选择"不使用任何介质"
[系统]
# 全部默认
机型="q35"
BIOS="OVMF (UEFI)"
添加EFI磁盘=0
SCSI控制器="VirtIO SCSI"
[硬盘]
删除当前磁盘
# 这里也可以全部默认，创建后再删除
[CPU]
核心=2
类别="host"
[内存]
内存(MiB)=2048
# HA 平时运行占用内存在 700MB 左右
# 也可以调大一点
[网络]
模型="VirtIO (半虚拟化)"
# 默认
# 半虚拟化和直通差不多, 比 E1000 效率高
[确认]
创建后启动=0
# 点击【完成】按钮
```

## 2. 调整配置

1. 在左侧窗口选中刚刚创建的虚拟机（名称是 "HA"），右边接着选择 "硬件"
2. 删除硬盘(如果创建时没删除):
   1. 选中刚刚创建虚拟机时候建立的硬盘（大小是 1G），点击【分离】
   2. 选中分离出来的硬盘，点击【移除】（分离后才能移除）
3. 选择 BIOS，调整 BIOS 为 UEFI 模式（haOS 要求的）

## 3. 安装 home-assistant OS

官方仓库: [home-assistant/operating-system](https://github.com/home-assistant/operating-system)

官方安装文档: [通用 x86-64](https://www.home-assistant.io/installation/generic-x86-64)

### 下载

官方发布页面: <https://github.com/home-assistant/operating-system/releases>

本文编写时最新版本为 14.1。

下载 `haos_ova-14.1.qcow2.xz`

下载后解压得到一个 `.qcow2` 文件。

### 上传

使用 `scp` 命令将 `.qcow2` 文件上传到 `/tmp` 目录（也可选择其他目录）

```sh
scp haos_ova-14.1.qcow2 root@<PVE_IP>:/tmp
```

### 导入文件

登录到 PVE 的终端 (Shell)

执行以下命令，其中 `100` 是虚拟机的编号，可在管理页面左侧查看。

```sh
cd /tmp
qm importdisk 100 haos_ova-14.1.qcow2 local-lvm
# Outputs:
# unused0: successfully imported disk 'local-lvm: vm-100-disk-0'
```

### 添加硬盘

在管理页面左侧点击 "HA" 虚拟机，右侧选择硬件，会看到一个未使用的磁盘 0，大小为 32G（可根据需要调整）。

双击未使用的磁盘 0，直接点击【添加】。

### 启动虚拟机

"选项-> 引导顺序-> 编辑"，设置启动项，选择 scsi0。

点击右上方【启动】按钮，等待系统启动完成。

启动成功后，在 Home Assistant 虚拟机的控制台（PVE 内的选项）中可以看到运行信息，包括 Web 端访问地址和端口。

如果虚拟机正常运行且 Home Assistant 启动成功，但控制台不显示 Web 地址和端口号而是显示错误提示，可能是网络问题，可以尝试为 Home Assistant 设置代理（例如在路由器中配置）后重启尝试。

首次启动需要安装较多组件，过程较慢，且可能会多次重启，请耐心等待。

## 4. 设置 haos

访问 haos 的网页端: `http://homeassistant.local:8124/`

首次进入需要设置用户信息。

使用设置好的用户名、密码登录。

### 安装 Terminal & SSH

设置 -> 加载项 -> 加载项商店 -> 搜索 "Terminal & SSH" -> 安装

推荐安装功能更强大的 "Advanced SSH & Web Terminal"

配置时需要设置 password 或 authorized_keys

```yaml
username: hassio
password: ""
authorized_keys: []
sftp: false
compatibility_mode: false
allow_agent_forwarding: false
allow_remote_port_forwarding: false
allow_tcp_forwarding: false
```

### 安装 HACS

HACS（Home Assistant Community Store）是 Home Assistant 的社区插件商店。

<https://www.hacs.xyz/docs/use/download/download/#to-download-hacs-ossupervised>

1. 点击 [链接](https://my.home-assistant.io/redirect/supervisor_addon/?addon=cb646a50_get&repository_url=https%3A%2F%2Fgithub.com%2Fhacs%2Faddons) 将 HACS 插件仓库添加到你的 Home Assistant。
   1. 当提示是否在 Home Assistant 中打开页面时，检查 URL 是否正确，然后选择打开链接。
   2. 在"缺少插件仓库"对话框中，选择"添加"。
   3. 现在你已经添加了允许下载 HACS 到 Home Assistant 的仓库。
2. 在 HACS 插件页面，选择"安装"。
3. 启动插件。
4. 导航到插件日志并按照其中的说明操作。

重启 HA。

Follow the steps on [setting up the HACS integration](https://www.hacs.xyz/docs/use/configuration/basic/#to-set-up-the-hacs-integration)
