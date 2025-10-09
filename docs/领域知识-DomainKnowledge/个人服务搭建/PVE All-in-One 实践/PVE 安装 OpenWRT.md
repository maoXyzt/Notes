# PVE 安装 OpenWRT

基于 PVE 8.3.0

选择的固件为 ImmortalWrt 23.05.4

> ImmortalWrt 有 rootf.tar.gz 的版本可以安装为 lxc 容器，
> lxc 容器直接运行在 PVE 内核上会比虚拟机少一点系统开销。
> 安装过程参考 <https://post.smzdm.com/p/a5xvwq93/>

## 0. 登录 PVE 的管理页面

`https://<IP>:8006`

## 1. 下载镜像

使用 [ImmortalWrt](https://github.com/immortalwrt/immortalwrt) 固件。

> * Default login address: `http://192.168.1.1` or `http://immortalwrt.lan`
> * username: "root"
> * password: none

下载地址：

途径 1:

* 进入 <https://firmware-selector.immortalwrt.org/>
* 搜索 `Generic x86/64`
* 找到 `.qcow2` 格式的的 ext4-efi 固件，下载

途径 2:

1. 进入 <https://downloads.immortalwrt.org/releases/>
2. 分别进入 {版本}, targets, x86, 64
3. 找到 .qcow2 格式的的 ext4-efi 固件，下载

> 格式说明：
>
> * x86-64: CPU 架构
> * `.qcow2`: 虚拟机支持.qcow2 格式的虚拟磁盘
> * `ext4`: 分区格式，ext4 格式方便好扩容
> * `efi`: 意思是用 uefi 启动。

> 编写本文时，下载的镜像为:
>
> * 版本: 23.05.4
> * 型号: Generic x86/64
> * 平台: x86/64
> * 版本: 23.05.4 (r28061-399f9a1db3)
> * 文件名: "immortalwrt-23.05.4-x86-64-generic-ext4-combined-efi.qcow2.gz"

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

### 3.1 导入文件

创建完成后，登录到 PVE 的终端 (Shell)

执行以下命令，其中 `100` 是虚拟机的编号，可在管理页面左侧查看。

```sh
cd /tmp
qm importdisk 100 immortalwrt-23.05.4-x86-64-generic-ext4-combined-efi.qcow2 local-lvm
# Outputs:
# unused0: successfully imported disk 'local-lvm: vm-100-disk-0'
```

### 3.2 添加硬盘

在管理页面左侧点击 "HA" 虚拟机，右侧选择硬件，会看到一个未使用的磁盘 0，大小为 32G（可根据需要调整）。

双击未使用的磁盘 0，直接点击【添加】。(硬盘如果是 ssd 建议勾选 ssd 仿真。)

### 3.3 安装 ImmortalWRT

"选项-> 引导顺序-> 编辑"，设置启动项，启用 scsi0 并设为第一位。

点击右上方【启动】按钮，等待系统启动完成。

## 4. 配置

### 4.1 配置网络

系统启动完成后，进入控制台。

默认网络为 192.168.1.1, 可以编辑 `/etc/config/network` 文件改, 把 IP 改成我们能访问的地址。

(192.168.50.20)

```sh
vi /etc/config/network
```

修改后重启网络服务

```bash
service network restart
```

之后打开浏览器输入 ip 地址就可以访问 ImmortalWrt。默认用户名是 "root"，密码是空。

### 4.2 配置网关、DNS

进入“网络”-“接口”设置界面，编辑“lan”（默认接口）。

常规设置：

* 协议: 静态地址
* IPv4 地址: 192.169.50.20
* IPv4 子网掩码: 255.255.255.0
* IPv4 网关: 192.168.50.1

高级设置 (这里以设为阿里公共 DNS 为例):

* 使用自定义的 DNS 服务器: 223.5.5.5

最后保存并应用，一定要保存并应用，不然不生效。

完成后可以在“网络诊断”中随意 ping 下，ping 通说明网络正常了。

### 4.3 关闭 DHCP

由于我们把 ImmortalWrt 当作旁路由器使用，所以关闭 DHCP 服务。

编辑“网络 -> 接口 -> lan”，在“DHCP-> 常规设置”中勾选“忽略此接口”。

### 4.4 关闭 IPv6

在透明代理中，IPv6 会导致 DNS 污染，因此现阶段我们先关闭 IPv6，将来再处理。

1. 网络-> 接口，修改 lan。在 DHCP 服务器-> IPv6 设置中，禁用所有服务并保存。
2. 网络-> DHCP/DNS，“过滤器”页面，勾选“过滤 IPv6 AAAA 记录”，保存并应用。

### 4.5 (可选) 更换皮肤

进入“系统”-“软件包”设置界面，先点击“更新列表”，然后搜索“argon”。

安装 luci-i18n-argon-config-zh-cn。

安装完成后刷新下网页，全新的皮肤就生效了。

## 5. 推荐插件

### 5.1 SmartDNS

在 “系统”->“软件包”中搜索 `luci-i18n-smartdns-zh-cn` 并安装。

### 5.2 OpenClash

> [OpenWrt 安装使用 OpenClash](https://blog.hellowood.dev/posts/openwrt-%E5%AE%89%E8%A3%85%E4%BD%BF%E7%94%A8-openclash/)

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

首次启动需要下载内核模块，下载完成后会自动重启。

#### (1) 配置 DNS

OpenClash 默认提供 7874 端口用于 DNS 查询；启动后会劫持 Dnsmasq，只保留自己作为 Dnsmasq 的上游；

但是目前的版本里并没有将已配置的 DNS 转发作为 OpenClash 的上游（参考 issue [启用 DNS 劫持后未将 Dnsmasq 中添加的 DNS 转发作为上游 DNS](https://github.com/vernesong/OpenClash/issues/2720)），这样会导致无法使用 SmartDNS 或其他上游 DNS，因此需要手动修改将 SmartDNS 作为 OpenClash 的上游服务器。

在 "服务"-> "OpenClash"-> "全局设置"-> "DNS 设置" 中，选择新增，设置自定义上游 DNS 服务器为 SmartDNS。

新增完成后，在该页面选择启用 “自定义上游 DNS 服务器”，这样，就可以使用 SmartDNS 作为主 DNS 服务器了；如果有其他的上游，也可以同样配置。

配置完成后，DNS 的查询流程为 客户端 -> Dnsmasq -> OpenClash -> SmartDNS -> 上游 DNS 服务器

#### (2) 配置运行模式

参考 OpenClash-常规设置，主要有 `Fake-IP` 和 `Redir-Host` 两种模式；
据其他用户的测试经验，开启了 OpenClash 使用 `Redir-Host` 会导致部分 UDP 流量超时，如王者荣耀/英雄联盟/吃鸡等使用 UDP 的应用超时或无法连接；
使用 `Fake-IP TUN` 模式则可以正常使用。

##### `Fake-IP`

当客户端发起请求查询 DNS 时，会先返回一个随机的保留地址，同时查询上游 DNS 服务器，如果需要代理则发送给代理服务器查询，然后再进行连接；客户端立即向 Fake-IP 发起的请求会被快速响应，节约了一次本地向 DNS 服务器查询的时间

运行模式有 TUN，增强和混合三种模式；区别在与 TUN 可以代理 UDP 流量

这个模式会导致客户端获取到的 DNS 查询到的结果与实际不一致，nslookup/dig 等的使用会受影响

##### `Redir-Host`

当客户端发起请求时，会并发查询 DNS，等待返回结果后再尝试进行规则判定和连接，如果需要代理，会使用 fallback 的 DNS 服务器再次查询；与不使用 OpenClash 相比，多了过滤，fallback 查询的时间，响应速度可能会变慢

有兼容，TUN 和混合三种模式，区别在与 TUN 可以代理 UDP 流量

### 5.3 DDNS

在 “系统”->“软件包”中搜索 luci-i18n-ddns-zh-cn 并安装。

DDNS 的更新由脚本执行，因此需要安装对应域名服务商的更新脚本；如 godaddy 的脚本是 ddns-scripts-godaddy；
官方提供的域名服务商脚本可以从 [Packagesindexnetwork—ip-addresses-and-names](https://openwrt.org/packages/index/network---ip-addresses-and-names) 查看

其他域名服务商可以在 GitHub 或恩山无线论坛中查找对应的软件

阿里云 DDNS 可在 <https://github.com/honwen/luci-app-aliddns/releases> 下载

### 5.4 AdBlock

luci-i18n-adblock-zh-cn

### 5.5 (Optional) passwall

luci-i18n-passwall-zh-cn

### 5.6 (Optional) homeproxy

luci-i18n-homeproxy-zh-cn

## 6. IPv6 支持

(todo)
