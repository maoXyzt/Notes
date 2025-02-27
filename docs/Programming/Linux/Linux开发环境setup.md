# Linux 开发环境 setup

## (1) Recommend

### 配置apt镜像

#### 全平台换源工具 `chsrc`

> [chsrc](https://github.com/RubyMetric/chsrc?tab=readme-ov-file#-%E5%AE%89%E8%A3%85)

```bash
# 使用维护团队测试的最快镜像站
# target: ubuntu, debian, rocky ...
./chsrc set <target> first
```

#### 手动换源

```bash
sudo apt install ca-certificates
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
```

> [配置apt镜像](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)

### Dependencies

```bash
# Ubuntu
sudo apt-get update
sudo apt-get install autoconf automake build-essential \
  cmake git libass-dev libbz2-dev libfontconfig1-dev libfreetype6-dev libfribidi-dev \
  libharfbuzz-dev libjansson-dev liblzma-dev libmp3lame-dev libogg-dev libopus-dev \
  libsamplerate-dev libspeex-dev libtheora-dev libtool libtool-bin libvorbis-dev \
  libx264-dev libxml2-dev m4 make nasm patch pkg-config tar yasm zlib1g-dev \
  python3 python3-pip python3-dev python3-setuptools zip
```

### Miniconda

- [Linux Installers](https://docs.conda.io/en/latest/miniconda.html#linux-installers)

### git 升级版本

- [install](https://git-scm.com/download/linux)
- [build from source](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### zsh

- 安装 [zsh](https://www.zsh.org/)
- [oh-my-zsh](https://github.com/maoXyzt/Notes/blob/master/docs/Programming/Linux/zsh%E5%B8%B8%E7%94%A8%E6%8F%92%E4%BB%B6.md)

### Node.js

> [Node.js安装](../JS-TS/Node.js%20安装.md)

- 利用[NVM](https://github.com/nvm-sh/nvm#installing-and-updating)安装
- 利用[FNM](https://github.com/Schniz/fnm?tab=readme-ov-file#installation)安装
- 直接安装[Download | node.js](https://nodejs.org/en/download/)

### Mackup: 配置备份/同步

- [Instruction](https://github.com/maoXyzt/Notes/blob/master/docs/Programming/Linux/Mackup%20%E5%90%8C%E6%AD%A5linux%E9%85%8D%E7%BD%AE.md)

### neovim

- [Installing-Neovim](https://github.com/neovim/neovim/wiki/Installing-Neovim#ubuntu)

### 配置全局 gitignore

- 配置方法: [global gitignore](https://github.com/maoXyzt/Notes/blob/master/docs/Programming/Git/global%20gitignore.md)

## (2) CLI tools

### 2.1 Rust CLI tools

**digest:**

Linux:

```bash
if ! [[ command -v rustup &> /dev/null ]]; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
fi
rustup update stable

export CARGO_INSTALL_ROOT=$HOME/_cargo_install_temp/

cargo install fd-find
cargo install --locked bat
cargo install ripgrep
cargo install du-dust
cargo install procs
cargo install atuin
cargo install git-delta
cargo install tealdeer
cargo install eza
cargo install bottom
cargo install xh --locked

sudo chown root:root $CARGO_INSTALL_ROOT/bin/*
sudo chmod 755 $CARGO_INSTALL_ROOT/bin/*
sudo mv $CARGO_INSTALL_ROOT/bin/* /usr/local/bin/

export CARGO_INSTALL_ROOT=

atuin import auto
```

macos

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
```

**list:**

- [rust](https://www.rust-lang.org/tools/install): 方便编译安装其他命令行工具
- [`fd`](https://github.com/sharkdp/fd#on-ubuntu): 替代`find`
- [`bat`](https://github.com/sharkdp/bat#from-source): 替代`cat`
- [`rg`](https://github.com/BurntSushi/ripgrep#installation): ripgrep，替代`grep`
- [`dust`](https://github.com/bootandy/dust#install): 替代`du`
- [`procs`](https://github.com/dalance/procs#cargo): 替代`ps`
- [`atuin`](https://github.com/ellie/atuin/blob/main/README.md#install): shell 历史记录增强
- [`delta`](https://dandavison.github.io/delta/installation.html#installation): syntax-highlighting git diff
- `tldr`:
  - (推荐) [`tealdeer`](https://dbrgn.github.io/tealdeer/installing.html)
  - (无需编译) [`tldr`](https://github.com/tldr-pages/tldr#how-do-i-use-it):
- ~~[`exa`](https://the.exa.website/install/linux): a modern replacement for `ls`~~ It's unmaintained. Use `eza` instead.
- [`eza`](https://github.com/eza-community/eza): a modern replacement for `ls`
- [`bottom`](https://github.com/ClementTsang/bottom): 图形化进程、系统monitor

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

### 2.2 Others

- ~~[`neofetch`](https://github.com/dylanaraps/neofetch): 获取并打印系统信息~~ Use `fastfetch` instead.
- [`fastfetch`](https://github.com/fastfetch-cli/fastfetch): Fastfetch is a neofetch-like tool for fetching system information and displaying it prettily.

```bash
# for Ubuntu only
sudo add-apt-repository ppa:zhangsongcui3371/fastfetch
sudo apt-get update
sudo apt-get install fastfetch
```

- [`fuck`](https://github.com/nvbn/thefuck#installation): thefuck，纠正输错的命令
