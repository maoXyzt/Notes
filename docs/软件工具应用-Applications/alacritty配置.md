# Alacritty 配置

配置文件位于:

* *nix: `~/.config/alacritty/alacritty.toml`
* Windows: `%APPDATA%\alacritty\alacritty.toml`

官方配置文档见: <https://alacritty.org/config-alacritty.html>

## Example

```toml
[general]
working_directory = 'C:\Users\<your-username>\'  # 设置默认工作目录

[window]
dimensions = { columns = 120, lines = 32 }
opacity = 0.85
dynamic_padding = true
blur = true                                # MacOS only

[font]
normal = { family = "Maple Mono NF CN", style = "Regular" }
size = 12.0

[terminal]
# 设置默认 shell.
# Windows 上默认是 PowerShell, 此处改为了 [Nu Shell](../Windows/windows平台使用nushell终端.md)
shell = { program = 'C:\Users\<your-username>\AppData\Local\Programs\nu\bin\nu.exe' }

[selection]
save_to_clipboard = true # 复制选中的文本到系统剪贴板; 否则只在终端内使用

[keyboard]
# 默认快捷键: <https://alacritty.org/config-alacritty-bindings.html>
bindings = [
  # 针对 Windows 平台，配置使用 Control/Shift + Insert 进行复制粘贴
  # 默认的 Ctrl + Shift + C/V 也可以使用
  { key = "Insert", mods = "Control", action = "Copy" },
  { key = "Insert", mods = "Shift", action = "Paste" },   # 默认操作为 PasteSelection, 不从系统剪贴板粘贴
  # 创建窗口
  { key = "T", mods = "Control | Shift", action = "CreateNewWindow" },
]

[mouse]
# 鼠标中键粘贴
bindings = [{ mouse = "Middle", action = "Paste" }]
```

## 问题

### 1. 无法响应鼠标点击

解决方案: <https://github.com/alacritty/alacritty/issues/1663#issuecomment-1917418514>

1. Go to <https://github.com/wez/wezterm/tree/main/assets/windows/conhost> and download `OpenConsole.exe` and `conpty.dll`
2. Put these files into your alacritty program directory (e.g. `c:\Program Files\Alacritty\`)
