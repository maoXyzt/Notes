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
[硬盘]
硬盘大小(GiB)=1
# 其实这个大小是多少无所谓，因为创建完虚拟机以后要把硬盘删掉
# 这里也可以全部默认
[CPU]
核心=2
[内存]
内存(MiB)=1024
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
2. 删除硬盘:
   1. 选中刚刚创建虚拟机时候建立的硬盘（大小是 1G），点击【分离】
   2. 选中分离出来的硬盘，点击【移除】（分离后才能移除）
3. 选择 BIOS，调整 BIOS 为 UEFI 模式（hassOS 要求的）

## 3. 安装 home-assistant OS

官方仓库: [home-assistant/operating-system](https://github.com/home-assistant/operating-system)

官方安装文档: [Generic x86-64](https://www.home-assistant.io/installation/generic-x86-64)

### 下载

官方 Release 页: <https://github.com/home-assistant/operating-system/releases>

本文编写时最新版本为 14.1。

下载 `haos_ova-14.1.qcow2.xz`

下载好以后解压得到一个 `.qcow2` 文件。

### 上传

1. 用 winscp 登录 pve
2. 把 `.qcow2` 文件传到 `/tmp` 目录（也可自选其他目录）

### 导入文件

登录到 PVE 的终端 (Shell)

执行以下命令，其中 `100` 是虚拟机的编号，可以在管理网页的左侧查看到。

```sh
cd /tmp
qm importdisk 100 haos_ova-14.1.qcow2 local-lvm
# Outputs:
# Successfully imported disk as 'unused0:local-lvm:vm-100-disk-0'
```

### 添加硬盘

在管理网页的左侧点击 "HA" 虚拟机，在右侧选择硬件，会发现出现一个未使用的磁盘0。

双击未使用的磁盘0，直接点击【添加】

### 启动虚拟机

点击右上方【启动】按钮，等待系统启动完成。

访问 haos 的网页端: <http://homeassistant.local:8123/>

第一次启动需要安装很多东西，过程比较慢，且中间会有多次重启，耐心等待即可。

## 4. 设置 haos

首次进入，需要先设置用户信息。

用设置好的用户名、密码登录。
