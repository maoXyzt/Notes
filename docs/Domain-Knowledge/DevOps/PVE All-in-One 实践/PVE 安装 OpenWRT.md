---
NoteStatus: draft
---

# PVE 安装 OpenWRT

基于 PVE 8.3.0

选择的固件为 ImmortalWrt 23.05.4

> ImmortalWrt 有 rootf.tar.gz 的版本可以安装为lxc容器，
> lxc容器直接运行在PVE内核上会比虚拟机少一点系统开销。
> 安装过程参考 <https://post.smzdm.com/p/a5xvwq93/>

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
名称="ImmortalWRT"
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
# cpu类型最好选择host，毕竟软路由大概率会涉及到aes解密，选择host可以调用aes指令集
[内存]
内存(MiB)=2048
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

双击未使用的磁盘 0，直接点击【添加】。(硬盘如果是 ssd 建议勾选 ssd 仿真。)

### 安装 ImmortalWRT

"选项-> 引导顺序-> 编辑"，设置启动项，启用 scsi0 并设为第一位。

点击右上方【启动】按钮，等待系统启动完成。

## 4. 配置

### 配置网络

系统启动完成后，进入控制台。

默认网络为 192.168.1.1, 可以编辑 `/etc/config/network` 文件改, 把 IP 改成我们能访问的地址。

(192.168.50.10)

```sh
vi /etc/config/network
```

修改后重启网络服务

```sh
service network restart
```

之后打开浏览器输入ip地址就可以访问 ImmortalWrt。默认用户名是 "root"，密码是空。

### 配置网关、DNS

进入“网络”-“接口”设置界面，编辑“lan”（默认接口）。

常规设置：

* 协议: 静态地址
* IPv4 地址: 192.169.50.10
* IPv4 子网掩码: 255.255.255.0
* IPv4 网关: 192.168.50.1

高级设置 (这里以设为阿里公共DNS为例):

* 使用自定义的 DNS 服务器: 223.5.5.5

最后保存并应用，一定要保存并应用，不然不生效。

完成后可以在“网络诊断”中随意ping下，ping通说明网络正常了。

### (可选) 更换皮肤

进入“系统”-“软件包”设置界面，先点击“更新列表”，然后搜索“argon”。

安装 luci-i18n-argon-config-zh-cn。

安装完成后刷新下网页，全新的皮肤就生效了。

## 5. 推荐插件

### 5.1 OpenClash

> <https://blog.hellowood.dev/posts/openwrt-%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8-openclash/>

OpenClash 是 Clash 的 OpenWrt 客户端。

可以在 OpenClash 仓库的 [Release](https://github.com/vernesong/OpenClash/releases) 页面选择对应的版本进行下载

本文编写时，安装的版本为 "v0.46.064"，需安装如下依赖:

```sh
#iptables
opkg update
opkg install coreutils-nohup bash iptables dnsmasq-full curl ca-certificates ipset ip-full iptables-mod-tproxy iptables-mod-extra libcap libcap-bin ruby ruby-yaml kmod-tun kmod-inet-diag unzip luci-compat luci luci-base

#nftables
opkg update
opkg install coreutils-nohup bash dnsmasq-full curl ca-certificates ip-full libcap libcap-bin ruby ruby-yaml kmod-tun kmod-inet-diag unzip kmod-nft-tproxy luci-compat luci luci-base
```

下载对应版本的 OpenClash 安装包，并安装。

```sh
wget https://github.com/vernesong/OpenClash/releases/download/v0.46.064/luci-app-openclash_0.46.064_all.ipk -O openclash.ipk
opkg update
opkg install openclash.ipk
```

重启。待重启完成后重新登录控制台，可以在服务菜单中看到 OpenClash

```sh
reboot
```
