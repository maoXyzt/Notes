---
type: note
aliases: []
created: 2026-02-27T19:37:22.000+0800
modified: 2026-05-05T22:55:26.291+0800
---

## 1 - 安装

通过包管理器安装 Fish Shell:

```bash
# Ubuntu
sudo add-apt-repository ppa:fish-shell/release-4
sudo apt update
sudo apt install fish
# MacOS
brew install fish
```

Mac 在安装之后，检查 `/etc/shells` 默认其中不含 `fish` 。将 `fish` 添加到其中:

```bash
echo "$(which fish)" | sudo tee -a /etc/shells
```

推荐安装 [Fisher](https://github.com/jorgebucaran/fisher): Fish Shell 的插件管理器

```bash
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
```

## 2 - 推荐插件安装

### 2.1 bass: 兼容 bash 命令

[bash](https://github.com/edc/bass)

```bash
fisher install edc/bass
```

使用时，在 bash 命令前加上 `bass` 即可

### 2.2 fish-git-abbr: 类似 oh-my-zsh 的 git 命令缩写

[fish-git-abbr](https://github.com/lewisacidic/fish-git-abbr)

```bash
fisher install lewisacidic/fish-git-abbr
```

注意, 部分命令有差别. 例如：
- zsh 中 `git status` 缩写为 `gst`, 而 fish 中缩写为 `gs`
