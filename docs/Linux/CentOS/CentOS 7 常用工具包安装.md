# CentOS7 常用工具包安装

## CentOS 常用工具包

CentOS7 安装时选择 `开发及生成工作站`，则下述工具包中除了 8 以外都已安装，仅仅需要升级。

### 1. `lrzsz` 虚拟机上传下载组件

支持从 windows 直接拖拽文件，相当好用

```bash
yum -y install lrzsz
```

使用方法：

```bash
# 上传
rz <文件名>
# 下载
sz <文件名>
```

### 2. gcc

nginx 之类由 c 语言开发的，编译的时候需要用到

```bash
yum -y install gcc-c++
```

### 3. PCRE

Perl 库，包括 perl 兼容的正则表达式库

```bash
yum -y install pcre pcre-devel
```

### 4. zlib

zlib 库提供了多种压缩和解压缩的方式

```bash
yum -y install zlib zlib-devel ruby
```

### 5. OpenSSL

OpenSSL 是一个强大的安全套接字层密码库，囊括主要的密码算法、常用的密钥和证书封装管理功能及 SSL 协议

```bash
yum -y install openssl openssl-devel patch
```

### 6. `wget`

安装 `wget` 下载工具

```bash
yum -y install wget
```

### 9. `lsof`

安装 lsof（list open files）是一个列出当前系统打开文件的工具

```bash
yum install lsof -y
```

### 10. `zip` `unzip`

```bash
yum install -y unzip zip
```

## 11. `pip`

首先需要安装一个叫“epel-release”的软件包，这个软件包会自动配置 yum 的软件仓库。EPEL (ExtraPackages for Enterprise Linux)是基于 Fedora 的一个项目，为“红帽系”的操作系统提供额外的软件包，适用于 RHEL、CentOS 和 Scientific Linux。说白了安装 epel-release 就是为了扩大软件包的搜索范围。

```bash
yum -y install epel-release
```

等到安装成功后再次安装 pip 就可以找到安装包并成功下载 pip 以及依赖的东西

```bash
yum install python-pip
```

在安装某些第三方包的时候需要 pip 升级成新的版本才能安装，因此将 pip 通过命令 `pip install --upgrade pip` 升级成最新的版本

```bash
pip install --upgrade pip
```
