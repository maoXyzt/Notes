# CentOS 7 安装/升级 Git 版本

在开始之前，先确认当前 Git 版本：

```bash
git --version
```

## 1. 通过 IUS 源安装

IUS (Inline with Upstream Stable) 是一个社区项目，为企业 Linux 发行版提供新版本软件的 RPM 包。该项目旨在为 Red Hat Enterprise Linux (RHEL) 和 CentOS 创建高质量的 RPM 包。

1. 卸载旧版本

```bash
sudo yum remove git*
```

2. 添加 IUS 源并安装

```bash
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install git2u-all
```

## 2. 源码编译安装

### 2.1 安装依赖

```bash
sudo yum groupinstall "Development Tools"
sudo yum -y install wget perl-CPAN gettext-devel perl-devel openssl-devel zlib-devel curl-devel expat-devel
```

### 2.2 下载源码

可以从官方镜像下载指定版本：
> <https://mirrors.edge.kernel.org/pub/software/scm/git/>

```bash
# 设置要安装的版本
export VER="2.22.0"
wget https://github.com/git/git/archive/v${VER}.tar.gz
tar -xvf v${VER}.tar.gz
cd git-${VER}
```

### 2.3 编译安装

```bash
./configure prefix=/usr/local/git/
make -j8
sudo make install
```

### 2.4 配置环境变量

将以下内容添加到 ~/.bashrc 或 /etc/profile：

```bash
export PATH=$PATH:/usr/local/git/bin
```

最后，确认安装成功：

```bash
git --version
```
