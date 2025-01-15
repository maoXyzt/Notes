---
NoteStatus: draft
---

# PVE 安装 OpenWRT

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

## 2. 下载镜像

可选择官方镜像或者用 Lean 大仓库自行编译的镜像

官方镜像: <https://archive.openwrt.org/>
Lean大仓库: <https://github.com/coolsnowwolf/lede>

编译详见
