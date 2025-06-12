# Linux 使终端支持 UTF-8 中文字符

## 1 - 检查系统是否支持 UTF-8

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

## 2 - 安装支持 UTF-8 的语言包

安装语言包:

```bash
sudo apt install language-pack-en
# 如果需要简体中文，安装: language-pack-zh-hans
# 如果需要繁体中文，安装: language-pack-zh-hant
```

再次执行 `locale -a` 命令，可以看到系统现在支持 "en_US.utf8" / "zh_CN.utf8" 编码。

## 3 - 设置系统编码

(1) 生成 locale 配置:

```bash
sudo locale-gen en_US.UTF-8
# 如果需要简体中文，生成: sudo locale-gen zh_CN.UTF-8
# 如果需要繁体中文，生成: sudo locale-gen zh_TW.UTF-8
```

(2) 编辑 `/etc/default/locale` 文件，添加:

```bash
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8

# 如果需要简体中文，配置为:
# LC_ALL=zh_CN.UTF-8
# LANG=zh_CN.UTF-8

# 如果需要繁体中文，配置为:
# LC_ALL=zh_TW.UTF-8
# LANG=zh_TW.UTF-8
```

或者，在终端的配置文件中添加 (`~/.bashrc` 或 `~/.zshrc`):

```bash
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8

# 如果需要简体中文，配置为:
# LC_ALL=zh_CN.UTF-8
# LANG=zh_CN.UTF-8

# 如果需要繁体中文，配置为:
# LC_ALL=zh_TW.UTF-8
# LANG=zh_TW.UTF-8
```

然后 `source ~/.bashrc` 或 `source ~/.zshrc` 使配置生效。

(3) 应用新的配置:

```bash
sudo locale-gen --purge
sudo update-locale
```

再次检查系统编码:

```bash
locale

# 命令输出内容的示例如下:
LANG=en_US.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=en_US.UTF-8
```
