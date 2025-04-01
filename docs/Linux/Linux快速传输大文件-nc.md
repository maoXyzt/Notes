# Linux 快速传输大文件: nc 命令

linux 下的文件传输，大家首先会想到 `rsync`、`scp` 之类的工具，但这类工具有一个特点——慢，因为这类工具都是加密传输，发送端加密，接收端解密，当我们传输一些非敏感文件的时候，完全可以不加密，直接在网络上传输。

## `nc` 发送接收数据

### 传输单个文件

接收端：

```bash
nc -l 45.55.0.86 9999 > jieshou.iso
```

> -l: 监听一个端口来接收数据
> -u: 不使用 TCP 而是使用 UDP 来进行数据连接（应该速度更快，没试）

整条命令的意思：本地开启 9999 端口来接收数据，把接收到的数据存到“jieshou.iso”文件里面。

发送端：

```bash
time nc 45.55.0.86 9999 < CentOS-6.9-x86_64-bin-DVD2.iso
```

命令最前面的 time 是用来检测该命令运行耗时的。

### 进度显示

若你文件实在太大，想看到传输进度，用 `pv`

```bash
yum install epel-release -y
yum install pv -y
```

接收端和发送端都可以分别显示

接收端：

```bash
nc -l 45.55.0.86 9999 |pv -b > jieshou.iso
```

发送端：

```bash
cat CentOS-6.9-x86_64-bin-DVD2.iso |pv -b | nc 45.55.0.86 9999
```

### 传输目录

接收端：

```bash
nc -l 45.55.0.86 9999 | pv -b > home.tar.gz
```

发送端：

```bash
tar -czf - /home/ | nc 45.55.0.86 9999
```

### 中转文件

路径：A > B > C

C 上：

```bash
nc -l 9999 > google_file.txt
```

B 上：

```bash
nc -l 9999 | nc (C的外网IP) 9999
```

A 上：

```bash
nc (B的外网IP) 9999 < google_file.txt
```
