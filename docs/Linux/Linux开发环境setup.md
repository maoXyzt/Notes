# Linux 开发环境 setup

本文介绍配置 Linux 开发环境的流程，按照步骤配置后，可初步完成开发环境搭建。

本文以 Ubuntu/Debian 系统为例，部分命令给出了 MacOS 版本。其他发行版请自行替换命令。

## 1 - 推荐

### 1.1 配置apt镜像

#### 1.1.1 全平台换源工具 `chsrc`

> [chsrc](https://github.com/RubyMetric/chsrc?tab=readme-ov-file#-%E5%AE%89%E8%A3%85)

```bash
# 使用维护团队测试的最快镜像站
# <target>: ubuntu, debian, rocky ...
chsrc set <target> first
```

#### 1.1.2 手动换源

```bash
sudo apt install ca-certificates
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
```

> [配置apt镜像](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)

### 1.2 依赖库&工具

```bash
# Ubuntu
sudo apt-get update
sudo apt-get install autoconf automake build-essential \
  cmake git libass-dev libbz2-dev libfontconfig1-dev libfreetype6-dev libfribidi-dev \
  libharfbuzz-dev libjansson-dev liblzma-dev libmp3lame-dev libogg-dev libopus-dev \
  libsamplerate-dev libspeex-dev libtheora-dev libtool libtool-bin libvorbis-dev \
  libx264-dev libxml2-dev m4 make nasm patch pkg-config tar yasm zlib1g-dev \
  python3 python3-pip python3-dev python3-setuptools zip curl wget
```

### 1.4 升级 Git 版本

- [install](https://git-scm.com/download/linux)
- [build from source](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 1.5 zsh

- 安装 [zsh](https://www.zsh.org/)
- 安装和配置 [oh-my-zsh](./zsh常用插件.md)

### 1.6 Mackup: 配置备份/同步

- [Instruction](./Mackup%20同步linux,macos配置.md)

### 1.7 配置全局 gitignore

- 配置方法: [global gitignore](../编程开发-Programming/Git/global%20gitignore.md)

## 2 - 可选依赖

根据个人开发需求，选择性安装。

### 2.1 Miniconda

- [Linux Installers](https://docs.conda.io/en/latest/miniconda.html#linux-installers)

### 2.2 Node.js

> [Node.js安装](../编程开发-Programming/Frontend/Node.js%20安装.md)

选择其中一种安装方式：

- 利用 [FNM](https://github.com/Schniz/fnm?tab=readme-ov-file#installation) 安装(推荐)

  ```bash
  curl -fsSL https://fnm.vercel.app/install | bash
  ```

- 利用 [NVM](https://github.com/nvm-sh/nvm#installing-and-updating) 安装
- 直接安装: [Node.js Download](https://nodejs.org/en/download/)

### 2.3 neovim

- [Installing-Neovim](https://github.com/neovim/neovim/wiki/Installing-Neovim#ubuntu)

## 3 - 命令行工具

### 3.1 Rust 命令行工具

#### 3.1.1 Linux 用户安装

```bash
if ! [[ command -v rustup &> /dev/null ]]; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
fi
rustup update stable

cargo install fd-find
cargo install bat --locked
cargo install ripgrep
cargo install du-dust
cargo install procs
cargo install atuin
cargo install git-delta
cargo install tealdeer
cargo install eza
cargo install bottom
cargo install xh --locked
cargo install zoxide --locked

atuin import auto
```

#### 3.1.2 MacOS 用户安装

```bash
if ! [[ command -v rustup &> /dev/null ]]; then
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
fi
rustup update stable

brew install fd
brew install bat
brew install ripgrep
brew install dust
brew install procs
brew install atuin
brew install git-delta
brew install tealdeer
brew install eza
brew install bottom
brew install xh
brew install zoxide fzf

atuin import auto
```

#### 3.1.2 工具说明

- [rust](https://www.rust-lang.org/tools/install): 方便编译安装其他命令行工具
- [`fd`](https://github.com/sharkdp/fd#on-ubuntu): 替代`find`
- [`bat`](https://github.com/sharkdp/bat#from-source): 替代`cat`
- [`rg`](https://github.com/BurntSushi/ripgrep#installation): ripgrep，替代`grep`
- [`dust`](https://github.com/bootandy/dust#install): 替代`du`
- [`procs`](https://github.com/dalance/procs#cargo): 替代`ps`
- [`atuin`](https://github.com/ellie/atuin/blob/main/README.md#install): shell 历史记录增强
- [`delta`](https://dandavison.github.io/delta/installation.html#installation): syntax-highlighting git diff
- `tldr`: 查阅命令的简单用法
  - (推荐) [`tealdeer`](https://github.com/tealdeer-rs/tealdeer?tab=readme-ov-file#docs-installing-usage-configuration)
  - (无需编译) [`tldr`](https://github.com/tldr-pages/tldr#how-do-i-use-it)
- [`eza`](https://github.com/eza-community/eza): a modern replacement for `ls`

  ```bash
  # linux x64
  wget -c https://github.com/eza-community/eza/releases/latest/download/eza_x86_64-unknown-linux-gnu.tar.gz -O - | tar xz
  sudo chmod +x eza
  sudo chown root:root eza
  sudo mv eza /usr/local/bin/eza
  ```

- [`bottom`](https://github.com/ClementTsang/bottom?ref=itsfoss.com#debianubuntu): 图形化进程、系统monitor

  ```bash
  # via snap
  sudo snap install bottom
  # To allow the program to run as intended
  sudo snap connect bottom:mount-observe
  sudo snap connect bottom:hardware-observe
  sudo snap connect bottom:system-observe
  sudo snap connect bottom:process-control
  ```

- [`xh`](https://github.com/ducaale/xh): 替代 `httpie`
- [`zoxide`](https://github.com/ajeetdsouza/zoxide): 替代 `autojump|z`, 基于目录访问频率进行智能匹配

> [zsh常用插件 | zoxide](./zsh常用插件.md#zoxide)

### 3.2 其他

### 3.2.1 zellij: 终端复用

> [zellij](https://github.com/zellij-org/zellij): 终端复用工具，比 tmux 好用

安装:

```bash
cargo install --locked zellij
```

### 3.2.2 fastfetch: 获取并打印系统信息

> [Fastfetch](https://github.com/fastfetch-cli/fastfetch): Fastfetch is a [Neofetch](https://github.com/dylanaraps/neofetch)-like tool for fetching system information and displaying it prettily.

```bash
# for Ubuntu only
sudo add-apt-repository ppa:zhangsongcui3371/fastfetch
sudo apt-get update
sudo apt-get install fastfetch
```

### 3.2.3 thefuck: 快速纠正输错的命令

> [thefuck](https://github.com/nvbn/thefuck#installation)

Linux 用户:

```bash
pip3 install thefuck --user
```

MacOS 用户:

```bash
brew install thefuck
```

### 3.2.4 Yazi: 命令行文件管理器

> [yazi: Blazing fast terminal file manager](https://github.com/sxyazi/yazi)
>
> [Installation | Yazi](https://yazi-rs.github.io/docs/installation/)

### 3.2.5 sttr: 字符串转换工具

> [sttr: cross-platform, cli app to perform various operations on string](https://github.com/abhimanyu003/sttr?tab=readme-ov-file#battery-installation)

Linux:

```bash
curl -sfL https://raw.githubusercontent.com/abhimanyu003/sttr/main/install.sh | sh
```

MacOS:

```bash
brew install abhimanyu003/sttr/sttr
```
