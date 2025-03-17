# win10系统下安装pycrypto包的方法

> 本文参考[win系统下python安装pycrypto包](https://blog.csdn.net/chen09122763/article/details/79017635)

在win10操作系统下，直接通过`pip install pycrypto`命令安装pycrypto包时，将有如下报错

> error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": <https://visualstudio.microsoft.com/downloads/>

可以通过安装mingw来解决。

## 1. 安装mingw

在下述网页下载Mingw-w64并安装

> <http://www.mingw-w64.org/doku.php>

## 2. 安装msys2

下载msys2，里面提供了bash的一些命令程序，因为在python编译时，会有一步chmod配置目录，如果不安装msys2会有报错。

> <http://www.msys2.org/>

## 3. 配置环境变量

配置环境变量，使得mingw64的bin和lib，msys2/usr/bin和lib可以被找到。

## 4. 修改python的配置

python安装目录下的`Lib\distutils`，修改`distutils.cfg`（没有，则创建）增加

```ini
[build]
compiler = mingw32
```
