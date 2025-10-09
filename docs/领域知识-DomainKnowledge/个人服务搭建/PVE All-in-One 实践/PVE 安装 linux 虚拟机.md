# PVE 安装 Linux 虚拟机

+ PVE 系统版本: 8.3.0
+ Linux 版本: archlinux-2025.10.01-x86_64

## 0 - 登录 PVE 的管理页面

`https://<IP>:8006`

## 1 - 下载镜像

根据官方文档的指导，下载系统镜像。

本文安装 ArchLinux 系统，所以下载 ArchLinux 的系统镜像，且使用了 aliyun.com 的镜像源。

> <https://archlinux.org/download/>

本文编写时 (2025-10-10)，下载得到的最新版本镜像文件为: `archlinux-2025.10.01-x86_64.iso`。

## 2 - 上传镜像

### 2.1 命令上传

这里用 `scp` 命令实现, 将镜像文件上传到 `/tmp` 目录:

```bash
scp archlinux-2025.10.01-x86_64.iso root@<PVE_IP>:/tmp
```

### 2.2 管理页面上传

也可以在管理页面中上传。

登录管理页面，在左侧面板展开 "Datacenter" -> "pve" -> "local (pve)"；
右侧面板中选择 "ISO Images", 点击 "Upload"；
在弹出的窗口中选择镜像文件，进行上传。

## 3 - 创建虚拟机

点击右上角 "Create VM" 按钮，进入创建虚拟机页面。

```ini
[General/一般]
"Name/名称"="ArchLinux"   # 虚拟机名称
[OS/操作系统]
选择 "Use CD/DVD disc image file (ISO)"
"Storage/存储"="local"
"ISO image/ISO 映像"=刚才上传的镜像文件
"Type/类型"="Linux" # 默认值，不用修改
[System/系统]
# 全部默认
[Disks/硬盘]
删除当前磁盘
# 这里也可以全部默认，创建后再删除
[CPU]
"Cores/核心"=2        # 可以大于物理核心数量
"Type/类别"="host"   # cpu类型最好选择host，毕竟软路由大概率会涉及到aes解密，选择host可以调用aes指令集
[Memory/内存]
"Memory (MiB)/内存 (MiB)"=4096  # 也可以调大一点
[Network/网络]
"Model/模型"="VirtIO (paravirtualized)/VirtIO (半虚拟化)"
# 默认
# 半虚拟化和直通差不多, 比 E1000 效率高
[Confirm/确认]
"Start after creation/创建后启动"=取消选择
# 点击【完成】按钮
```

点击 "Finish/完成" 按钮，进入虚拟机详情页面。

## 4 - 调整配置

1. 在左侧窗口选中刚刚创建的虚拟机（名称是 "ArchLinux"），右边接着选择 "Hardware/硬件"
2. 选择 "Hardware", 删除硬盘(如果创建时没删除):
   1. 选中刚刚创建虚拟机时候建立的硬盘（大小是 64G），点击【Detach/分离】
   2. 选中分离出来的硬盘，点击【Remove/移除】（分离后才能移除）
3. 选择 "BIOS"，调整 BIOS 为 UEFI 模式 (建议改，但不改也行)
4. 点击 "Add" 添加硬盘, Storage 为 "local-lvm", Size 为 128G

完成后，点击 "Start/启动" 按钮，启动虚拟机。

按照 Linux 安装镜像的引导，完成 Linux 系统的安装。
