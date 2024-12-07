# Mackup 同步linux配置

## 0. 关于mackup

> [Mackup](https://github.com/lra/mackup)

> [What does it really do to my files](https://github.com/lra/mackup#bullsht-what-does-it-really-do-to-my-files)

## 1. 安装

> [INSTALL.md](https://github.com/lra/mackup/blob/master/INSTALL.md)

macOS:

```bash
brew install mackup
```

其他系统(通过pip安装):

```bash
pip3 install --upgrade mackup
```

在 Ubuntu 系统中，用 pip 会默认安装到用户的 HOME 目录下。如果希望安装到系统路径中，需要添加 `--system` flag (其他平台则不用)

## 2. 用法

```bash
# Backup your application settings.
mackup backup

# Restore your application settings on a newly installed workstation.
# * 在新机器上恢复配置
mackup restore

# Copy back any synced config file to its original place.
mackup uninstall

# Display the list of applications supported by Mackup.
mackup list

# Display the list of applications supported by Mackup.
mackup -h
```

## 3. 配置

> [Configuration](https://github.com/lra/mackup/blob/master/doc/README.md)

配置文件在`~/.mackup.cfg`

### 3.1 Storage

可指定 Mackup 使用的用于存放配置文件的存储类型，默认为`dropbox`。

如果使用文件系统，需要进行如下配置：

```ini
[storage]
engine = file_system
path = some/folder/in/your/home
# or path = /some/folder/in/your/root
```

注意：不需要使用引号把路径包裹起来。

>
> 如何更换所使用的存储引擎:
>
> https://github.com/lra/mackup/blob/master/doc/README.md#switching-storage
>

### 3.2 Applications

#### (1) 只同步几个应用

在 `.mackup.cfg` 配置文件的 `[applications_to_sync]` 一节中，添加需要同步的应用，每个占一行：

```ini
# Example, to only sync SSH and Adium:
[applications_to_sync]
ssh
adium
```

#### (2) 不同步几个应用

在 `.mackup.cfg` 配置文件的 `[applications_to_ignore]` 一节中，添加不同步的应用，每个占一行：

```ini
# Example, to not sync SSH and Adium:
[applications_to_ignore]
ssh
adium
```

#### (3) 添加对任意应用/文件/目录的同步支持

可以对 HOME 目录之下的任意文件/目录添加同步支持。

创建 `~/.mackup` 目录，在其中添加配置文件

```bash
mkdir ~/.mackup
touch ~/.mackup/my-files.cfg
```

配置文件，内容如下：

```ini
[application]
name = My personal synced files and dirs

[configuration_files]
bin
.hidden
```

可以通过 `mackup list` 检查是否已添加成功

```bash
$ mackup list
Supported applications:
[...]
 - my-files
[...]
```

## 4. Tips

### (1) `.mackup.cfg` 也可以被同步。

在新平台上初始化时，先手动将 `.mackup.cfg` 复制到 `~/.mackup.cfg` 再执行 `mackup restore`。

```bash
cp ~/dotfiles/Mackup/.mackup.cfg ~/
```

### (2) 移除一个已同步应用

1. 先 `mackup uninstall`
2. 然后修改 `~/mackup.cfg`
3. 最后 `mackup backup`
