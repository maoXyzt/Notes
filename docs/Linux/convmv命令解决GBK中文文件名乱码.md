# convmv 命令解决 GBK 中文文件名乱码

## 问题原因

在 Linux 系统中，如果文件名是中文，且编码为 GBK，那么文件系统中显示时会出现乱码。这个问题常见于 Windows 系统创建的文件，在 Linux 系统中使用时。

这是因为 Linux 系统默认使用 UTF-8 编码，所以需要转码。

用 `convmv` 命令可以进行文件名转码。

## 安装 convmv

```bash
yum install convmv
```

## 文件名编码转换命令

```bash
convmv -f GBK -t UTF-8 -r --nosmart --notest <目标目录>
```

* `-f`: from，当前文件名编码
* `-t`: to，目标文件名编码
* `--nosmart`: 如果文件名编码已经是 UTF-8, 则忽略转换
* `-r`: 递归式地包含所有子目录
* `--notest`: 如果不提供这个参数，则只会列出需要转换的文件，不做实际转换
