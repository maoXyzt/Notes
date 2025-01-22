---
NoteStatus: draft
---

# PVE 安装 OpenWRT

基于 PVE 8.3.0

## 0. 登录 PVE 的管理页面

`https://<IP>:8006`

## 1. 下载镜像

使用 [ImmortalWrt](https://github.com/immortalwrt/immortalwrt) 固件。

> * Default login address: <http://192.168.1.1> or <http://immortalwrt.lan>
> * username: root
> * password: none

下载地址：

途径1:

* 进入 <https://firmware-selector.immortalwrt.org/>
* 搜索 `Generic x86/64`
* 找到 .qcow2 格式的的 ext4-efi 固件，下载

途径2:

1. 进入 <https://downloads.immortalwrt.org/releases/>
2. 分别进入 {版本}, targets, x86, 64
3. 找到 .qcow2 格式的的 ext4-efi 固件，下载

> 格式说明：
>
> * x86-64: CPU 架构
> * `.qcow2`: 虚拟机支持.qcow2格式的虚拟磁盘
> * `ext4`: 分区格式，ext4格式方便好扩容
> * `efi`: 意思是用 uefi 启动。

> 编写本文时，下载的镜像为:
>
> * 版本: 23.05.4
> * 型号: Generic x86/64
> * 平台: x86/64
> * 版本: 23.05.4 (r28061-399f9a1db3)
> * 文件名: immortalwrt-23.05.4-x86-64-generic-ext4-combined-efi.qcow2.gz

## 2. 上传

解压下载的镜像，得到 `.qcow2` 格式的文件。

上传 `.qcow2` 到虚拟机。

这里用 `scp` 命令实现:

```bash
scp immortalwrt-23.05.4-x86-64-generic-ext4-combined-efi.qcow2 root@<PVE_IP>:/tmp
```

## 3. 创建虚拟机

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
SCSI控制器="VirtIO SCSI Single"
[硬盘]
删除当前磁盘
# 这里也可以全部默认，创建后再删除
[CPU]
核心=2
类别="host"
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

### 导入文件

创建完成后，登录到 PVE 的终端 (Shell)

执行以下命令，其中 `100` 是虚拟机的编号，可在管理页面左侧查看。

```sh
cd /tmp
qm importdisk 100 immortalwrt-23.05.4-x86-64-generic-ext4-combined-efi.qcow2 local-lvm
# Outputs:
# unused0: successfully imported disk 'local-lvm: vm-100-disk-0'
```

### 添加硬盘

在管理页面左侧点击 "HA" 虚拟机，右侧选择硬件，会看到一个未使用的磁盘 0，大小为 32G（可根据需要调整）。

双击未使用的磁盘 0，直接点击【添加】。
