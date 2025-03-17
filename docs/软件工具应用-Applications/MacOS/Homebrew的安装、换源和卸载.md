# Homebrew 的安装、换源和卸载

## 1. 安装

### 1.1 命令行安装

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 1.2 使用 .pkg 文件安装

在 [Release](https://github.com/Homebrew/brew/releases) 页面下载

### 1.3 使用阿里源安装

用 [阿里源](https://developer.aliyun.com/mirror/homebrew) 安装

```bash
# 从阿里云下载安装脚本并安装 Homebrew
git clone https://mirrors.aliyun.com/homebrew/install.git brew-install
/bin/bash brew-install/install.sh
rm -rf brew-install
```

## 2. 配置阿里源

配置 repo 使用阿里源

```bash
git -C "$(brew --repo)" remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git
```

配置 `~/.bash_profile` 或 `~/.zshrc` 文件

```bash
# bash 用户
HOMEBREW_API_DOMAIN="https://mirrors.aliyun.com/homebrew-bottles/api"
HOMEBREW_BREW_GIT_REMOTE="https://mirrors.aliyun.com/homebrew/brew.git"
HOMEBREW_CORE_GIT_REMOTE="https://mirrors.aliyun.com/homebrew/homebrew-core.git"
HOMEBREW_BOTTLE_DOMAIN="https://mirrors.aliyun.com/homebrew/homebrew-bottles"
```

配置后执行 `brew update` 更新

配置 tap 仓库（非必需，非开发者无需配置）

```bash
# 绝大部分用户无需额外配置 tap 仓库
# 如果您需要使用 Homebrew 的开发命令，则按照如下命令配置 homebrew/core 和 homebrew/cask 镜像。
brew tap -v --custom-remote --force-auto-update homebrew/core https://mirrors.aliyun.com/homebrew/homebrew-core.git
brew tap -v --custom-remote --force-auto-update homebrew/cask https://mirrors.aliyun.com/homebrew/homebrew-cask.git

# 其他 tap 仓库按需配置即可
brew tap -v --custom-remote --force-auto-update homebrew/cask-fonts https://mirrors.aliyun.com/homebrew/homebrew-cask-fonts.git
brew tap -v --custom-remote --force-auto-update homebrew/cask-versions https://mirrors.aliyun.com/homebrew/homebrew-cask-versions.git
brew tap -v --custom-remote --force-auto-update homebrew/command-not-found https://mirrors.aliyun.com/homebrew/homebrew-command-not-found.git
brew tap -v --custom-remote --force-auto-update homebrew/services https://mirrors.aliyun.com/homebrew/homebrew-services.git
```

回退到默认配置

```bash
unset HOMEBREW_BREW_GIT_REMOTE
git -C "$(brew --repo)" remote set-url origin https://github.com/Homebrew/brew

unset HOMEBREW_API_DOMAIN
unset HOMEBREW_CORE_GIT_REMOTE
BREW_TAPS="$(BREW_TAPS="$(brew tap 2>/dev/null)"; echo -n "${BREW_TAPS//$'\n'/:}")"
for tap in core cask{,-fonts,-versions} command-not-found services; do
    if [[ ":${BREW_TAPS}:" == *":homebrew/${tap}:"* ]]; then
        brew tap --custom-remote "homebrew/${tap}" "https://github.com/Homebrew/homebrew-${tap}"
    fi
done

brew update

# 如果您之前永久配置了 HOMEBREW 环境变量，还需要在对应的配置文件中，将对应的 HOMEBREW 环境变量配置行删除
```

## 3. 卸载

卸载脚本

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
```

## 4. FAQ

### 1) `brew update` 不能升级 brew 版本

回退更换的源到默认配置后，再执行 `brew update` 即可升级 brew 版本。（然后再把源更换回来）
