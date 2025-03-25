# win10 系统下安装 pycrypto 包的方法

> 本文参考 [win 系统下 python 安装 pycrypto 包](https://blog.csdn.net/chen09122763/article/details/79017635)

在 win10 操作系统下，直接通过 `pip install pycrypto` 命令安装 pycrypto 包时，将有如下报错

> error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": <https://visualstudio.microsoft.com/downloads/>

可以通过安装 mingw 来解决。

## 1. 安装 mingw

在下述网页下载 Mingw-w64 并安装

> <http://www.mingw-w64.org/doku.php>

## 2. 安装 msys2

下载 msys2，里面提供了 bash 的一些命令程序，因为在 python 编译时，会有一步 chmod 配置目录，如果不安装 msys2 会有报错。

> <http://www.msys2.org/>

## 3. 配置环境变量

配置环境变量，使得 mingw64 的 bin 和 lib，msys2/usr/bin 和 lib 可以被找到。

## 4. 修改 python 的配置

python 安装目录下的 `Lib\distutils`，修改 `distutils.cfg`（没有，则创建）增加

```ini
[build]
compiler = mingw32
```
