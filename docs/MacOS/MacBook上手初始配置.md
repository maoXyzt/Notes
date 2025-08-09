---
NoteStatus: draft
---

# MacBook 上手初始配置

系统版本: macOS Sequoia (15.5)

## 触控

设置 - 辅助功能 - 指针控制 - 触控板选项...:

* 开启“使用触控板进行拖移”，“拖移样式”选择“三指拖移”

设置 - 触控板 - 滚动缩放

* 关闭“自然滚动”

设置 - 触控板 - 更多手势

* 调度中心: 选择“四指向上轻扫”
* App Exposé: 选择“四指向下轻扫”

~~下载 “Scroll Reverser” 软件~~

* 安装后，按提示给予权限
* 在 “滚动” 中，勾选“启用 Scroll Reverser”
* 在 “软件” 中，勾选“登录时启动”

## 键盘

设置 - 键盘

* “键重复速率”：调到最快；“重复前延迟”：调到第二短。（否则按住一个键时，感觉很迟钝）
* “按下 🌐 键时”: 选择“更改输入法”
* “输入法”: 按需添加

设置 - 键盘 - 键盘快捷键 - 功能键: 开启 “将 F1, F2 等键为标准功能键”

关闭“长按按键出现变音符号”功能: 终端运行 `defaults write -g ApplePressAndHoldEnabled -bool false`

## 字体

Maple Mono: 下载 NF CN hinted 版本（字体名: Maple Mono NF CN）

## 软件

免费或可以不购买:

* Homebrew: [Homebrew 的安装、换源和卸载](./Homebrew的安装、换源和卸载.md)
* iTerm2: 终端
* Edge 浏览器

* BitWarden: 密码管理
* Tencent Lemon: 清理垃圾文件
* Rime 输入法

* Snipaste: 截图工具 (v2 版本免费)

* Kawa: Input Method 快捷键管理 <https://github.com/hatashiro/kawa>

* AlDente: 电池管理
* Keka: 解压缩

* CheatSheet: 快捷键提示
* Apparency:

* IINA: 视频播放器

App Store 软件:

* 超级右键 Lite: 右键菜单增强
* AutoSwitchInput Lite: 自动切换输入法
* NTFS Disk by Omi NTFS: NTFS 格式读写

收费软件:

* Alfred: 启动器
* Bartender 5: 管理菜单栏图标
* iStat Menus: 系统监控
* Magnet: 窗口管理
* One Switch: 快捷切换功能

## 命令行工具

参考: [Linux开发环境setup](../Linux/Linux开发环境setup.md)
