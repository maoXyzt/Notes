# Linux 下多线程下载工具 - Axel

Axel 是 Linux 下一个不错的轻量级高速下载工具，支持 HTTP/FTP/HTTPS/FTPS 协议，支持多线程下载、断点续传，且可以从多个地址或者从一个地址的多个连接来下载同一个文件。适合网速不给力时多线程下载提高下载速度。

## 安装

Ubuntu:

```bash
sudo apt install axel
```

## 使用方法

```bash
axel 参数 文件下载地址
```

比较常用可选参数：

* `-s`: 设置最大下载速度，如果限制到 512KB/s，则填写 512000
* `-n`: 指定连接数
* `-o`: 指定另存为目录，或者指定的目录+文件名
* `-H`: 指定 header
* `-U`: 指定 useragent
* `-q`: 静默模式
* `-a`: 更改默认进度条样式

如果下载过程中下载中断可以再执行下载命令即可恢复上次的下载进度。
