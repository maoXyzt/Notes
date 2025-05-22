# Windows 平台使用 nushell 终端

Nushell: <https://www.nushell.sh/>

Windows 平台用 powershell 作为 Windows Terminal 的默认终端时，启动太慢了(~5000ms)，所以改用 nushell 作为默认终端。

## 1 - 安装

```bash
# 用 Winget 安装
winget install nushell
# 或者 用 Chocolatey 安装
choco install nushell
# 或者 用 Scoop 安装
scoop install nushell
```

安装好之后，用 `nu` 命令即可启动 nushell

### 1.1 - 配置为默认终端

安装完 nushell 后，Windows Terminal 会自动添加相应的配置文件。

在 Windows Terminal 的设置中把 nushell 的配置文件设置为默认配置文件即可。

### 1.2 - 初始化 nushell 的配置文件

nushell 有2个配置文件，分别为 `config.nu` 和 `env.nu`。

* `config.nu` 是 nushell 的配置文件，用于配置 nushell 的外观和行为。可通过 `$nu.config-path` 查看配置文件路径。
* `env.nu` 是 nushell 的环境变量配置文件，用于配置 nushell 的环境变量。可通过 `$nu.env-path` 查看环境变量配置文件路径。

一些有用的配置和 alias:

```bash
#--------------------
# Default editor
#--------------------
export-env { $env.config.buffer_editor = "code" }   # 设置默认编辑器为 vscode

#--------------------
# Aliases
#--------------------
alias ll = ls -a
alias la = ls -a

# Git alias

alias g = git
alias ga = git add
alias gaa = git add --all

alias gc = git commit -v
alias gc! = git commit -v --amend
alias gcn! = git commit -v --no-edit --amend
alias gca = git commit -v -a

alias gcb = git checkout -b

alias gd = git diff
alias gds = git diff --staged

alias gf = git fetch
alias gfa = git fetch --all --prune

alias gl = git pull

alias gp = git push

alias gst = git status
```

## 2 - 扩展插件

为了与 Linux 平台的终端体验尽可能一致，安装一些正在 Linux 平台上使用的插件。

### 2.1 主题

使用 [starship](https://starship.rs/) 作为 nushell 的主题，与 Linux 平台保持一致。

> [Linux/zsh常用插件.md｜3.2：主题starship](../Linux/zsh常用插件.md#32-主题starship)

```bash
choco install starship
```

安装好 starship 后，在 nushell 的配置文件的**末尾**添加以下配置:

```bash
#--------------------
# starship
#--------------------
mkdir ($nu.data-dir | path join "vendor/autoload")
starship init nu | save -f ($nu.data-dir | path join "vendor/autoload/starship.nu")
```

使用预设主题 [Bracketed Segments](https://starship.rs/presets/bracketed-segments)：

```bash
starship preset bracketed-segments -o ~/.config/starship.toml
```

重启 nushell 后，即可看到效果。

### 2.2 插件

#### (1) 历史记录增强: atuin

> [atuin](https://atuin.sh/)

用 cargo 安装 atuin (需要先安装 [rust](https://rustup.rs/))

```bash
cargo install atuin
```

安装好 atuin 后，先在 nushell 中执行如下命令:

```bash
mkdir ~/.local/share/atuin/
atuin init nu | save ~/.local/share/atuin/init.nu
```

之后在 nushell 的配置文件中添加以下配置：

```bash
source ~/.local/share/atuin/init.nu
```

重启 nushell 后生效。

#### (2) 命令行文件管理器: yazi

> [yazi](https://yazi-rs.github.io/)

在 Windows 平台上，yazi 依赖于 Git 的 `file(1)` 实现： `file.exe`。

> file.exe 可能在如下位置之一:
>
> * 通过 [official installer](https://git-scm.com/download/win) 安装的 Git: `C:\Program Files\Git\usr\bin\file.exe`
> * 通过 [scoop](https://scoop.sh/) 安装的 Git: `C:\Users\<Username>\scoop\apps\git\current\usr\bin\file.exe`

安装 Git，并在 `config.nu` 中配置 `YAZI_FILE_ONE` 环境变量指向 `file.exe` 的路径：

```bash
export-env { $env.YAZI_FILE_ONE = 'C:/Program Files/Git/usr/bin/file.exe' }
```

安装 yazi 和可选依赖:

```bash
winget install sxyazi.yazi
# Install the optional dependencies (recommended):
winget install Gyan.FFmpeg 7zip.7zip jqlang.jq sharkdp.fd BurntSushi.ripgrep.MSVC junegunn.fzf ajeetdsouza.zoxide ImageMagick.ImageMagick
```

配置 nushell 的 `config.nu` 文件:

```bash
#--------------------
# yazi
#--------------------
def --env y [...args] {
  let tmp = (mktemp -t "yazi-cwd.XXXXXX")
  yazi ...$args --cwd-file $tmp
  let cwd = (open $tmp)
  if $cwd != "" and $cwd != $env.PWD {
    cd $cwd
  }
  rm -fp $tmp
}
```

安装完成后，输入 `y` 即可启动 yazi。

* 按 `q` 键退出 yazi，并切换当前目录到 yazi 的目录;
* 按 `Q` 键退出 yazi，并回到进入 yazi 前的目录;
* 按 `F1` 或 `~` 键打开帮助菜单;

其他快捷键参见 [Keybindings](https://yazi-rs.github.io/docs/quick-start#keybindings)

### (3) 目录跳转: zoxide

> [zoxide](https://github.com/ajeetdsouza/zoxide)

安装 zoxide:

```bash
winget install ajeetdsouza.zoxide
```

先编辑 `env.nu` 文件(`$nu.env-path`)，在文件末尾加入:

```bash
zoxide init nushell | save -f ~/.zoxide.nu
```

然后配置 nushell 的 `config.nu` 文件，在文件末尾加入:

```bash
source ~/.zoxide.nu
```

(可选) 安装 `fzf` 以支持补全和交互式选择:

```bash
winget install fzf
```

使用方法:

```bash
z foo              # cd into highest ranked directory matching foo
z foo bar          # cd into highest ranked directory matching foo and bar
z foo /            # cd into a subdirectory starting with foo

zi foo             # cd with interactive selection (using fzf)
```

## 3 - 配置文件示例

打开配置文件并(用 VSCode)编辑: `code $nu.config-path`

```bash
# config.nu
#
# Installed by:
# version = "0.103.0"
#
# This file is used to override default Nushell settings, define
# (or import) custom commands, or run any other startup tasks.
# See https://www.nushell.sh/book/configuration.html
#
# This file is loaded after env.nu and before login.nu
#
# You can open this file in your default editor using:
# config nu
#
# See `help config nu` for more options
#
# You can remove these comments if you want or leave
# them for future reference.

#--------------------
# Default editor
#--------------------
export-env { $env.config.buffer_editor = "code" }

#--------------------
# Aliases
#--------------------

alias ll = ls -a
alias la = ls -a

# Git alias

alias g = git
alias ga = git add
alias gaa = git add --all

alias gc = git commit -v
alias gc! = git commit -v --amend
alias gcn! = git commit -v --no-edit --amend
alias gca = git commit -v -a

alias gcb = git checkout -b

alias gd = git diff
alias gds = git diff --staged

alias gf = git fetch
alias gfa = git fetch --all --prune

alias gl = git pull

alias gp = git push

alias gst = git status

#--------------------
# Rust mirrors
#--------------------
export-env { $env.RUSTUP_UPDATE_ROOT = 'https://mirrors.aliyun.com/rustup/rustup' }
export-env { $env.RUSTUP_DIST_SERVER = 'https://mirrors.aliyun.com/rustup' }

#--------------------
# atuin
#--------------------
source ~/.local/share/atuin/init.nu

#--------------------
# yazi
#--------------------
export-env { $env.YAZI_FILE_ONE = 'C:/Program Files/Git/usr/bin/file.exe' }
def --env y [...args] {
  let tmp = (mktemp -t "yazi-cwd.XXXXXX")
  yazi ...$args --cwd-file $tmp
  let cwd = (open $tmp)
  if $cwd != "" and $cwd != $env.PWD {
    cd $cwd
  }
  rm -fp $tmp
}

#--------------------
# starship
#--------------------
mkdir ($nu.data-dir | path join "vendor/autoload")
starship init nu | save -f ($nu.data-dir | path join "vendor/autoload/starship.nu")
```
