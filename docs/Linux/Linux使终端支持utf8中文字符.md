# Linux 使终端支持 UTF-8 中文字符

## 1 - 检查系统是否支持 UTF-8 中文字符

安装 `locales` 包

```bash
sudo apt update
sudo apt install locales
```

用 `locale` 命令查看当前系统编码:

```bash
locale
# 命令输出内容的示例如下:
LANG=
LANGUAGE=
LC_CTYPE="POSIX"
LC_NUMERIC="POSIX"
LC_TIME="POSIX"
LC_COLLATE="POSIX"
LC_MONETARY="POSIX"
LC_MESSAGES="POSIX"
LC_PAPER="POSIX"
LC_NAME="POSIX"
LC_ADDRESS="POSIX"
LC_TELEPHONE="POSIX"
LC_MEASUREMENT="POSIX"
LC_IDENTIFICATION="POSIX"
LC_ALL=
```

用 `locale` 命令查看系统支持的编码:

```bash
locale -a
# 命令输出内容的示例如下:
# C
# C.UTF-8
# POSIX
```

## 2 - 安装中文语言包

安装中文语言包:

```bash
sudo apt install language-pack-zh-hans
# 如果需要繁体中文，安装: language-pack-zh-hant
# 建议同时也安装英文语言包: language-pack-en
```

再次执行 `locale -a` 命令，可以看到系统现在支持 "zh_CN.utf8" 编码。

## 3 - 设置系统编码

设置系统编码:

```bash
sudo locale-gen zh_CN.UTF-8
```

编辑 `/etc/default/locale` 文件，添加:

```bash
LANG=zh_CN.UTF-8
LC_ALL=zh_CN.UTF-8
```

应用新的配置:

```bash
sudo locale-gen --purge
sudo update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8
```
