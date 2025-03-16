# CentOS 7 安装最新版本的Git

首先查看当前git版本

```bash
git --version
```

## Install the latest git from the IUS repository

IUS is a community project that provides RPM packages for newer versions of select software for Enterprise Linux distributions. The aim of the project is to create high-quality RPM packages for Red Hat Enterprise Linux (RHEL) and CentOS.

```bash
sudo yum remove git*
sudo yum -y install  https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install  git2u-all
```

## Install the latest git from source

Install dependency packages required

```bash
sudo yum groupinstall "Development Tools"
sudo yum -y install wget perl-CPAN gettext-devel perl-devel  openssl-devel  zlib-devel
```

Download and install git

```bash
export VER="2.22.0"
wget https://github.com/git/git/archive/v${VER}.tar.gz
tar -xvf v${VER}.tar.gz
rm -f v${VER}.tar.gz
cd git-*
sudo make install
```
