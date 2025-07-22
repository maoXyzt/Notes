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

[keyboard]
# 默认快捷键: <https://alacritty.org/config-alacritty-bindings.html>
bindings = [
  # 针对 Windows 平台，配置使用 Alt + C/V 或者 Insert 和 Shift + Insert 进行复制粘贴
  # 默认的 Ctrl + Shift + C/V 也可以使用
  { key = "C", mods = "Alt", action = "Copy" },
  { key = "V", mods = "Alt", action = "Paste" },
  { key = "Insert", action = "Copy" },
  { key = "Insert", mods = "Shift", action = "Paste" },   # 默认操作为 PasteSelection，只对 Linux 有效
  # 创建 Tab 和窗口
  { key = "T", mods = "Control", action = "CreateNewTab" },            # 只在 MacOS 上有效
  { key = "T", mods = "Control | Shift", action = "CreateNewWindow" },
]

[mouse]
bindings = [
  # 鼠标右键粘贴
  { mouse = "Right", action = "Paste" }
]
```
