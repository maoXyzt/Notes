# asdf版本管理工具的安装和使用

asdf是一个可用于管理多种运行时(runtime)版本的命令行工具，可通过插件扩展支持多种语言。

适用系统：Linux、MacOS

> 源码：https://github.com/asdf-vm/asdf
>
> 文档：https://asdf-vm.com

## 0. 太长不看版

以下的步骤将安装asdf和asdf的erlang、elixir插件，然后安装并全局启用最新版本的erlang和elixir。

(1) 安装

```bash
sudo apt install curl git unzip automake autoconf
# Install v0.8.1
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.8.1
```

(2) 配置`~/.bashrc` 或 `~/.zshrc`

`~/.bashrc`:

```bash
. $HOME/.asdf/asdf.sh
. $HOME/.asdf/completions/asdf.bash
```

`~/.zshrc`:

```bash
. $HOME/.asdf/asdf.sh
# append completions to fpath
fpath=(${ASDF_DIR}/completions $fpath)
# initialise completions with ZSH's compinit
autoload -Uz compinit && compinit
```

(3) 安装 Elixir

```bash
asdf plugin add elixir
asdf install elixir 1.12
asdf global elixir 1.12
```

(4) 安装 Erlang

```bash
asdf plugin add erlang
asdf install erlang 23.3
asdf global erlang 23.3
```

(5) 验证安装

```bash
asdf list erlang
erl
asdf list elixir
elixir -v
```

## 1. 安装

> [Manage asdf - Install (asdf-vm.com)](https://asdf-vm.com/#/core-manage-asdf?id=install)

### 1.1 安装依赖：curl、git、unzip

```bash
sudo apt install curl git unzip
```

### 1.2 安装

本文编写时的最新版本：v0.8.1

```bash
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.8.1
```

或者下载整个仓库并checkout到最新版本

```bash
git clone https://github.com/asdf-vm/asdf.git ~/.asdf
cd ~/.asdf
git checkout "$(git describe --abbrev=0 --tags)"
```

### 1.3 配置环境

#### bash

添加以下内容到`~/.bashrc`

```bash
. $HOME/.asdf/asdf.sh
. $HOME/.asdf/completions/asdf.bash
```

重启bash或重新加载配置：`source ~/.bashrc`

#### zsh

添加以下内容到`~/.zshrc`

```bash
. $HOME/.asdf/asdf.sh
# append completions to fpath
fpath=(${ASDF_DIR}/completions $fpath)
# initialise completions with ZSH's compinit
autoload -Uz compinit && compinit
```

重启zsh或重新加载配置：`zsh ~/.zshrc`

### 1.4 更新

```bash
asdf update
```

### 1.5 卸载

移除添加到`.bashrc`/`.zshrc`中的上述内容。

执行以下命令删除asdf的相关文件

```bash
rm -rf ${ASDF_DATA_DIR:-$HOME/.asdf} ~/.tool-versions
```

## 2. 使用

### 2.1 插件管理

#### Add

```bash
asdf plugin add <name>
# asdf plugin add erlang
```

如果需要的插件不在 plugins repository 中，可以通过指定repository的URL来添加：

```bash
asdf plugin add <name> <git-url>
# asdf plugin add elm https://github.com/vic/asdf-elm
```

> [All Plugins (asdf-vm.com)](https://asdf-vm.com/#/plugins-all)

#### List

```bash
asdf plugin list
# asdf plugin list
# java
# nodejs
```

```bash
asdf plugin list --urls
# asdf plugin list
# java            https://github.com/halcyon/asdf-java.git
# nodejs          https://github.com/asdf-vm/asdf-nodejs.git
```

#### Update

```bash
asdf plugin update --all
```

```bash
asdf plugin update <name>
# asdf plugin update erlang
```

#### Remove

```bash
asdf plugin remove <name>
# asdf plugin remove erlang
```

### 2.2 版本管理

#### Install

```bash
asdf install <name> <version>
# asdf install erlang 17.3
```

```bash
asdf install <name> latest
# asdf install erlang latest
```

```bash
asdf install <name> latest:<version>
# asdf install erlang latest:17
```

#### List

列出已安装的

```bash
asdf list <name>
# asdf list erlang
```

列出所有可用版本

```bash
asdf list all <name>
# asdf list all erlang
```

```bash
asdf list all <name> <version>
# asdf list all erlang 17
```

显示最新稳定版本

```bash
asdf latest <name>
# asdf latest erlang
```

```bash
asdf latest <name> <version>
# asdf latest erlang 17
```

#### Set Current Version

```bash
asdf global <name> <version> [<version>...]
asdf shell <name> <version> [<version>...]
asdf local <name> <version> [<version>...]
# asdf global elixir 1.2.4
```

`global`：版本信息写入`$HOME/.tool-versions`

`shell`：版本信息写入环境变量`ASDF_${LANG}_VERSION`（例如`ASDF_ELIXIR_VERSION=1.4.0`），仅对当前shell有效

`local`：版本信息写入`$PWD/.tool-versions`

#### Show Current Version

```bash
asdf current
# asdf current
# erlang 17.3 (set by /Users/kim/.tool-versions)
# nodejs 6.11.5 (set by /Users/kim/cool-node-project/.tool-versions)
```

```bash
asdf current <name>
# asdf current erlang
# 17.3 (set by /Users/kim/.tool-versions)
```

#### Uninstall

```bash
asdf uninstall <name> <version>
# asdf uninstall erlang 17.3
```

#### 版本切换的原理：Shims

当用`asdf`安装package时，会为在`$ASDF_DATA_DIR/shims`目录下（默认为`~/.asdf/shims`）为package的每个可执行程序创建shims。

通过`asdf.sh`/`asdf.fish`等启动脚本已将该目录添加到了`$PATH`中，因此已安装的程序可以被当前环境所用。

Shims本身是对`asdf exec`这个helper的简单包装，执行该命令并传给它插件的名称和package中可执行程序的路径。

`asdf exec`确定package的版本（根据 global/local 的`.tool-versions`或环境变量），得到以下信息，然后后执行程序。

- 可执行程序的最终路径，位于package安装目录中（该行为受到插件中的`exec-path`callback 控制）
- 执行时的环境（由插件的 `exec-env` 脚本提供）

> 注意：
>
> 由于该系统使用`exec`，package中任何需要被shell `source`而非执行的脚本都不能通过shim包装而是需要直接访问。可以借助asdf命令`which`和`where`来帮助获得安装的package的路径：
>
> ```bash
> # returns path to main executable in current version
> source $(asdf which ${PLUGIN})/../script.sh
> ```
>
> ```bash
> # returns path to the package installation directory
> source $(asdf where ${PLUGIN} $(asdf current ${PLUGIN}))/bin/script.sh
> ```

##### 绕过asdf shims

动机：

- 每次执行都需要通过shim，需要寻找并解析`.tool-versions`文件，会影响执行效率。
- 程序通过`which my-command`命令无法得到自己的位置，而是得到shim的位置，会造成一些程序的问题。
- 希望进入目录时自动设置环境变量。

使用`asdf-direnv`插件，可结合`direnv`与`asdf`。具体安装与用法见链接：

> [asdf-community/asdf-direnv: direnv plugin for the asdf version manager (github.com)](https://github.com/asdf-community/asdf-direnv)

## 3. 配置

> [Configuration (asdf-vm.com)](https://asdf-vm.com/#/core-configuration)

### 3.1 `.tool-versions`

当存在一个`.tool-versions`文件时，该文件定义的版本会被用于当前目录及其子目录。

全局默认值定义在`$HOME/.tool-versions`

### 3.2 `$HOME/.asdfrc`

asdf的配置文件，包括以下配置选项：

- legacy_version_file
- use_release_candidates
- always_keep_download

### 3.3 环境变量

- `ASDF_CONFIG_FILE`: 默认为`~/.asdfrc`

- `ASDF_DEFAULT_TOOL_VERSIONS_FILENAME`: 默认为`.tool-versions`
- `ASDF_DIR`: 默认为`~/.asdf`。安装 asdf 脚本的目录。
- `ASDF_DATA_DIR`: 默认为`~/.asdf`。安装 plugins, shims 和 installs 的目录。

## 4. 其他命令

通过`asdf` 或 `asdf help`查看
