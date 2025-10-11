# ArchLinux 简单安装教程

本文参考 [官方指南](https://wiki.archlinuxcn.org/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97) 编写，简化了一些不关键的步骤。

如果希望了解每一步背后的原理，请参考官方指南。

## 1 - 下载镜像

官方下载页面: <https://archlinux.org/download/>

可选择 aliyun.com 的镜像源 (`.iso` 格式)。

本文编写时 (2025-10-10)，下载得到的最新版本镜像文件为: `archlinux-2025.10.01-x86_64.iso`。

## 2 - 引导启动

可以参考 [制作 U 盘启动盘](../../领域知识-DomainKnowledge/个人服务搭建/PVE%20All-in-One%20实践/制作U盘启动盘.md) 的教程。

主板/虚拟机配置使用 UEFI 模式引导。

## 3 - 安装系统

用 ISO 镜像启动后, 选择 "Arch Linux install medium" 并按 Enter 进入安装环境。

此时将以 `root` 用户身份登录 shell, 默认 shell 是 zsh。

### 3.1 设置网络

查看当前的网络配置:

```bash
ip link
```

可以用 `ping archlinux.org` 检查网络是否连通。

### 3.2 更新系统时间

执行如下命令更新系统时间，也会显示当前的时间和时区:

```bash
timedatectl
```

### 3.3 创建硬盘分区

查看识别到的硬盘:

```bash
fdisk -l
# Outputs:

# Disk /dev/sda: 128 GiB, 137438953472 bytes, 268435456 sectors
# Disk model: QEMU HARDDISK
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
#
#
# Disk /dev/loop0: 957.07 MiB, 1003560960 bytes, 1960080 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
```

其中以 `rom`、`loop` 或者 `airootfs` 结尾的设备可以被忽略。
以 `rpmb`、`boot0` 或者 `boot1` 结尾的 `mmcblk*` 设备也可以被忽略。

用 `cfdisk` 命令修改分区表:

```bash
cfdisk /dev/<要被分区的磁盘>  # e.g. /dev/sda
```

执行后, 会显示 `/dev/<要被分区的磁盘>` 的分区表。

如果出现 "Select label type" 的提示, 选择 "gpt" (UEFI 模式下必须使用 gpt 分区表)。之后会显示分区表。

选择菜单中的 "new" 选项, 然后选择分区类型为 "primary"。

建议创建如下分区 (先按分区类型和大小创建分区, 之后再挂载):

+ EFI 系统分区
  + 分区类型: EFI System
  + 建议大小: 1 GiB
  + 分区: `/dev/efi_system_partition` (分区时根据实际情况自动生成)
  + 挂载点: `/boot`
+ 交换空间
  + 分区类型: Linux swap
  + 建议大小: >= 4 GiB
  + 分区: `/dev/swap_partition` (分区时根据实际情况自动生成)
  + 挂载点: `[SWAP]`
+ 根目录
  + 分区类型: Linux root (x86-64)
  + 建议大小: 设备剩余空间, 至少 23-32 GiB
  + 分区: `/dev/root_partition` (分区时根据实际情况自动生成)
  + 挂载点: `/`

按如上操作创建分区后，再用 `fdisk -l` 命令查看, 可以看到类似如下的分区表:

```bash
Device        Start       End   Sectors  Size Type
/dev/sda1      2048   2099199   2097152    1G EFI System
/dev/sda2   2099200  10487807   8388608    4G Linux swap
/dev/sda3  10487808 268433407 257945600  123G Linux root (x86-64)
```

根据上述分区表可知:

+ `/dev/efi_system_partition` 实际为 `/dev/sda1`
+ `/dev/swap_partition` 实际为 `/dev/sda2`
+ `/dev/root_partition` 实际为 `/dev/sda3`

### 3.4 格式化分区

创建上述分区后，需要格式化分区。

对照分区类型和分区设备，执行如下命令格式化分区:

```bash
# /dev/efi_system_partition 格式化为 Fat32 分区
mkfs.fat -F 32 /dev/sda1
# /dev/swap_partition 格式化为 swap 分区
mkswap /dev/sda2
# /dev/root_partition 格式化为 btrfs 分区 (根据需求更改类型)
mkfs.btrfs /dev/sda3  # 如果分区非空，需要加上 -f 参数
```

### 3.5 挂载分区

注意需要先挂载 root 分区，再挂载 boot 分区, 再挂载其他分区。否则可能遇到安装完成后无法启动的问题。

```bash
# /dev/root_partition 挂载到 /mnt
mount /dev/sda3 /mnt
# /dev/efi_system_partition 挂载到 /mnt/boot
mount --mkdir /dev/sda1 /mnt/boot
# 挂载 /dev/swap_partition 分区
swapon /dev/sda2
```

> 如果挂载错了，可以用如下命令取消挂载:
> `umount /mnt/boot; umount /mnt; swapoff /dev/sda2`

可以用 `lsblk -f` 命令查看当前的挂载情况

### 3.6 选择软件包的镜像站

下载大陆的镜像站列表:

```bash
curl -L 'https://archlinux.org/mirrorlist/?country=CN&protocol=https' -o /etc/pacman.d/mirrorlist
```

镜像列表文件位于 `/etc/pacman.d/mirrorlist`, 其中越靠前的镜像站优先级越高。

编辑该文件, 取消注释其中的镜像站, 并保存。

### 3.7 安装必需的软件包

```bash
pacstrap -K /mnt base linux linux-firmware
```

### 3.8 生成 fstab 文件

生成 fstab 文件，使需要的文件系统在启动时被自动加载:

```bash
genfstab -U /mnt > /mnt/etc/fstab
```

执行完后, 检查一下 `/mnt/etc/fstab` 文件, 确保内容正确。

### 3.9 chroot 的新安装的系统

```bash
arch-chroot /mnt
```

### 3.10 设置时区

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc   # 生成 /etc/adjtime
```

### 3.11 安装引导程序

选择使用 [GRUB](https://wiki.archlinuxcn.org/wiki/GRUB)

```bash
pacman -S grub efibootmgr
```

执行下面的命令将 GRUB EFI 应用 `grubx64.efi` 安装到 `/boot/EFI/GRUB`:

```bash
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
```

安装完成后，需要生成主配置文件 `/boot/grub/grub.cfg`

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

### 3.12 其他 (可选)

```bash
# 新系统没有文本编辑器, 需要安装一个
pacman -S vim
# 设置主机名为 arch
echo arch > /etc/hostname
# 修改 root 密码
passwd
# > 输入新密码
```

安装网络管理器

```bash
pacman -S networkmanager
cat >> /etc/hosts << EOF
127.0.0.1 localhost
::1 localhost
127.0.1.1 arch
EOF
```

SSH 服务

```bash
pacman -S openssh
echo PermitRootLogin yes >> /etc/ssh/sshd_config
```

## 4 - 重新启动计算机

```bash
# 退出 chroot 环境
exit
# 重启计算机
reboot
```

重启后，输入账号密码，进入系统。

执行以下命令恢复网络以及开启 ssh 服务:

```bash
systemctl enable NetworkManager --now
systemctl enable sshd --now
```

## 5 - 桌面环境配置

桌面环境可选 KDE Plasma、GNOME、Xfce 等。此处我选择 GNOME。

```bash
pacman -S gnome gnome-extra   # 安装 GNOME 桌面环境
systemctl enable gdm
pacman -S gnome-software-packagekit-plugin  # 安装 GNOME 软件中心
```

再安装思源字体，防止中文乱码:

```bash
pacman -S adobe-source-han-serif-cn-fonts
```

由于桌面不允许 root 用户登录，需要创建一个普通用户:

```bash
useradd -m localuser -G wheel
sed -i 's/# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
passwd localuser
# > 输入新密码
```

之后重启电脑，即可进入桌面环境。

## 6 - 安装常用软件

中文输入法

```bash
pacman -S fcitx-im fcitx-configtool  # 安装输入法框架和配置程序
pacman -S fcitx-libpinyin  # 安装拼音输入法
# 设置环境变量
cat >> /etc/environment << EOF
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
EOF
```

## 7 - 基本命令

同步并更新系统

```bash
pacman -Syu
```

清理软件包缓存

```bash
# 删除旧版本软件包 (位于 /var/cache/pacman/pkg 目录下), 保留当前版本
pacman -Sc
```
