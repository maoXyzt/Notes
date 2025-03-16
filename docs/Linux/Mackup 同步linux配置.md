# Mackup 同步 linux 配置

Mackup 是一个命令行工具，用于备份和恢复应用程序的配置文件。

> 项目主页: [Mackup](https://github.com/lra/mackup)
>
> [What does it really do to my files](https://github.com/lra/mackup#bullsht-what-does-it-really-do-to-my-files)

## 1. 安装

> [INSTALL.md](https://github.com/lra/mackup/blob/master/INSTALL.md)

macOS:

```bash
brew install mackup
```

其他系统(通过 pip 安装):

```bash
pip3 install --upgrade mackup
```

在 Ubuntu 系统中，用 pip 会默认安装到用户的 HOME 目录下。如果希望安装到系统路径中，需要添加 `--system` flag (其他平台则不用)

## 2. 用法

备份当前系统的配置文件：

```bash
# Backup your application settings.
mackup backup
```

在新机器上恢复配置:

```bash
# Restore your application settings on a newly installed workstation.
mackup restore
```

取消同步（把 Mackup 建立的软链接恢复为普通文件）：

```bash
# Copy back any synced config file to its original place.
mackup uninstall
```

列出支持的应用：

```bash
# Display the list of applications supported by Mackup
mackup list
```

查看帮助：

```bash
# Display the help information for Mackup
mackup -h

```

## 3. 配置

> [Configuration](https://github.com/lra/mackup/blob/master/doc/README.md)

配置文件在 `~/.mackup.cfg`

### 3.1 Storage

可指定 Mackup 使用的用于存放配置文件的存储类型，默认为 `dropbox`。

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
> <https://github.com/lra/mackup/blob/master/doc/README.md#switching-storage>
>

### 3.2 应用(Applications)同步范围配置

#### (1) 只同步指定的应用

在 `.mackup.cfg` 配置文件的 `[applications_to_sync]` 一节中，添加需要同步的应用，每个占一行。

例如，只同步 SSH 和 Adium:

```ini
# ~/.mackup.cfg
[applications_to_sync]
ssh
adium
```

配置后，只有 `ssh` 和 `adium` 的配置文件会被同步。

#### (2) 配置不同步的应用

在 `.mackup.cfg` 配置文件的 `[applications_to_ignore]` 一节中，添加不同步的应用，每个占一行：

例如，不同步 SSH 和 Adium:

```ini
# ~/.mackup.cfg
[applications_to_ignore]
ssh
adium
```

配置后，除了 `ssh` 和 `adium` 的配置文件，其他的都会被同步。

#### (3) 添加自定义的同步应用

可以将希望同步的文件、目录作为一个自定义应用添加到 Mackup 中。

支持对 `$HOME` 目录之下的任意文件/目录添加同步支持。

创建 `~/.mackup` 目录，在其中创建配置文件，例如 `my-files.cfg`:

```bash
mkdir ~/.mackup
touch ~/.mackup/my-files.cfg
```

配置文件的内容如下，在 `[configuration_files]` 中添加需要同步的文件：

```ini
# ~/.mackup/my-files.cfg
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

### (1) `.mackup.cfg` 也可以被同步

在新平台上初始化时，先手动将 `.mackup.cfg` 复制到 `~/.mackup.cfg` 再执行 `mackup restore`。

```bash
cp ~/dotfiles/Mackup/.mackup.cfg ~/
```

### (2) 移除一个已同步应用

1. 先 `mackup uninstall`
2. 然后修改 `~/mackup.cfg`
3. 最后 `mackup backup`
