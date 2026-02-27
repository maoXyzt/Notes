---
type: note
aliases: []
created: 2026-02-27T19:37:22.000+0800
modified: 2026-02-27T19:38:15.418+0800
---

# Fish Shell 安装

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

[Fisher](https://github.com/jorgebucaran/fisher): Fish Shell 的插件管理器

```bash
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
```
