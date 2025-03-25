# Linux下安装Go环境

> Golang官网下载地址：<https://golang.org/dl/>

打开官网下载地址选择对应的系统版本, 复制下载链接
   `go1.10.3.linux-amd64.tar.gz`：<https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz>

## 1

`cd`进入你用来存放安装包的目录。然后执行

```
wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz
```

## 2

执行`tar`解压到`/usr/loacl`目录下，得到`go`文件夹

```
tar -C /usr/local -zxvf  go1.10.3.linux-amd64.tar.gz
```

## 3

添加`/usr/loacl/go/bin`目录到PATH变量中。添加到`/etc/profile` 或`$HOME/.profile`都可以

```
// 习惯用vim，没有的话可以用命令`sudo apt-get install vim`安装一个
vim /etc/profile
// 在最后一行添加
export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
// wq保存退出后source一下
source /etc/profile
```

## 4

执行`go version`，如果显示版本号，则Go环境安装成功。
