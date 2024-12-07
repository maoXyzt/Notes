## 通过 IUS 源安装

1、确认你的当前 Git 版本

在终端输入：

```bash
git --version
```

2、卸载旧版本

```bash
sudo yum remove git*
```

3、添加 IUS CentOS 7 repo 并安装Git

```bash
sudo yum -y install  https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install  git2u-all
```

4、检查当前 Git 版本

```bash
git --version
```
## 2. 编译安装

### 2.1 安装依赖

```bash
yum install curl-devel expat-devel gettext-devel openssl-devel zlib-devel gcc perl-ExtUtils-MakeMaker
```

### 2.2 下载源码

> https://mirrors.edge.kernel.org/pub/software/scm/git/

```bash
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-<version>.tar.gz
tar -zxvf git-<version>.tar.gz
cd git-<version>
```

### 2.3 安装

```bash
./configure prefix=/usr/local/git/
make -j8
make install
```

### 2.4 配置

```bash
export PATH=$PATH:/usr/local/git/bin
```
