# CentOS7 常用工具包安装

## CentOS常用工具包

CentOS7 安装时选择`开发及生成工作站`，则下述工具包中除了8以外都已安装，仅仅需要升级。

### 1.虚拟机上传下载组件( 支持从windows直接拖拽文件，相当好用)

```bash
yum -y install lrzsz  

rz+文件名(上传)
sz+文件名(下载)
```


### 2.gcc (nginx之类由c语言开发的，编译的时候需要用到)
yum -y install gcc-c++ 


### 3.PCRE (Perl库，包括 perl 兼容的正则表达式库)
yum -y install pcre pcre-devel 


### 4.zlib (zlib库提供了很多种压缩和解压缩的方式)
yum -y install zlib zlib-devel ruby


### 5.openssl (OpenSSL 是一个强大的安全套接字层密码库，囊括主要的密码算法、常用的密钥和证书封装管理功能及SSL协议)
yum -y install openssl openssl-devel patch


### 6.安装wget下载工具
yum -y install wget


### 7.使用systemctl自动补全服务名称( 因为CentOS7的默认安装类型是最小安装，所以默认没有自动补全的功能)
yum install -y bash-completion


### 8.centos  64位系统兼容32位运行程序（aapt）
yum install -y zlib.i686 libstdc++.i686


### 9.安装lsof（list open files）是一个列出当前系统打开文件的工具
yum install lsof -y


### 10.zip unzip
yum install -y unzip zip

## CentOS 安装pip

首先需要安装一个叫“epel-release”的软件包，这个软件包会自动配置yum的软件仓库。EPEL (ExtraPackages for Enterprise Linux)是基于Fedora的一个项目，为“红帽系”的操作系统提供额外的软件包，适用于RHEL、CentOS和Scientific Linux。说白了安装epel-release就是为了扩大软件包的搜索范围。

yum -y install epel-release

等到安装成功后再次安装pip就可以找到安装包并成功下载pip以及依赖的东西

yum install python-pip

在安装某些第三方包的时候需要pip升级成新的版本才能安装，因此将pip通过命令pip install --upgrade pip升级成最新的版本

[root@localhost bin]$pip install --upgrade pip