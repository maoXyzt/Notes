# Homebrew 的安装、换源和卸载

## 1 - 安装 Homebrew

### 1.1 命令行安装

#### (1) 用官方安装脚本

[官网](https://brew.sh/) 安装命令:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### (2) 用清华源安装

> [TUNA Homebrew 软件仓库](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)
> [TUNA Homebrew Bottles 软件仓库](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew-bottles/): Homebrew 二进制预编译包的镜像。

```bash
# homebrew 镜像源
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
# homebrew bottles 镜像源
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
```

说明:

自 Homebrew 4.0 版本起 (2023-02-16 发布), `HOMEBREW_INSTALL_FROM_API=1` 已成为默认行为。

仅当需要使用 brew 开发者命令 (指 `brew edit`, `brew create`, `brew audit` 等需要直接操作 `homebrew/core` 仓库文件的命令。) 时，
才需要克隆 `homebrew/core` 仓库。

除了 contributors 和 希望深度定制 Homebrew 的用户外，绝大部分用户无需克隆 `homebrew/core` 仓库。
因此也不需要再配置 `HOMEBREW_CORE_GIT_REMOTE`。

> brew 仓库的区别:
>
> - `homebrew/brew`: 这是 Homebrew 核心命令行工具本身的代码仓库。它包含了 brew 命令的源代码，定义了 install, uninstall, search 等所有命令的逻辑。`HOMEBREW_BREW_GIT_REMOTE` 用于指定该仓库的镜像源。运行 `brew update` 时，会从该仓库拉取最新的代码更新。
> - `homebrew/core`: 这是 Homebrew 官方软件包配方 (Formula) 的仓库。它包含了成千上万个 .rb 文件，每个文件都描述了如何安装一个特定的软件（如 git, node, python）。`HOMEBREW_CORE_GIT_REMOTE` 用于指定该仓库的镜像源。

```bash
# 从镜像下载安装脚本并安装 Homebrew / Linuxbrew
git clone --depth=1 <https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/install.git> brew-install
/bin/bash brew-install/install.sh
rm -rf brew-install
```

### 1.2 使用 .pkg 文件安装

在 [Release](https://github.com/Homebrew/brew/releases) 页面下载

## 2 - 更换已有的 Homebrew 的镜像源

配置 repo 使用清华源

```bash
git -C "$(brew --repo)" remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git
```

配置 `~/.bash_profile` 或 `~/.zprofile` 文件

```bash
# homebrew 镜像源
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
# homebrew bottles 镜像源
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
```

配置后执行 `brew update` 更新

## 3 - 回退到默认配置

回退到默认配置:

```bash
# brew 程序本身，Homebrew / Linuxbrew 相同
unset HOMEBREW_API_DOMAIN
unset HOMEBREW_BREW_GIT_REMOTE
git -C "$(brew --repo)" remote set-url origin https://github.com/Homebrew/brew

# 以下针对 macOS 系统上的 Homebrew
unset HOMEBREW_CORE_GIT_REMOTE
BREW_TAPS="$(BREW_TAPS="$(brew tap 2>/dev/null)"; echo -n "${BREW_TAPS//$'\n'/:}")"
for tap in core cask; do
    if [[ ":${BREW_TAPS}:" == *":homebrew/${tap}:"* ]]; then  # 只复原已安装的 Tap
        brew tap --custom-remote "homebrew/${tap}" "https://github.com/Homebrew/homebrew-${tap}"
    fi
done

# 重新拉取远程
brew update

# 注：重置回默认远程后，用户应该删除 shell 的 profile 设置中的环境变量 `HOMEBREW_BREW_GIT_REMOTE` 和 `HOMEBREW_CORE_GIT_REMOTE`,
# 以免运行 `brew update` 时远程再次被更换。
```

## 4 - 卸载 Homebrew

卸载脚本

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
```

## 5 - FAQ

### 1) `brew update` 不能升级 brew 版本

回退更换的源到默认配置后，再执行 `brew update` 即可升级 brew 版本。（然后再把源更换回来）
