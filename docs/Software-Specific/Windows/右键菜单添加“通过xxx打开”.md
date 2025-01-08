# 右键菜单添加 “通过 xxx 打开”

以添加 “通过 Neovim 打开” 为例。

涉及到以下注册表分支：

- `HKEY_CLASSES_ROOT\*\shell`: options to the right-click menu for files
- `HKEY_CLASSES_ROOT\Folder\shell`: options to the right-click menu for folders
- `HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell`: options to the right-click menu for desktop

## 一、右键打开文件

### 1. 打开注册表编辑器

快捷键 `win +R` 打开 “运行”，输入 `regedit` 开启 “注册表编辑器”。

定位到

- `HKEY_CLASSES_ROOT\*\shell`: options to the right-click menu for files
- `HKEY_CLASSES_ROOT\Folder\shell`: options to the right-click menu for folders
- `HKEY_CLASSES_ROOT\Directory\Background\shell\` 或 `HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell`: options to the right-click menu for desktop

### 2. 新建菜单项

在 shell 下新建 `项`，命名为 `Open with neovim`

可在右侧窗口中修改 `(默认)` 的值为 <菜单显示名称>，例如：

```text
通过 Neovim 打开
```

### 3. 设置命令

在 `Open with neovim` 下新建 `项`，命名为 `command`。

在右侧窗口中修改 `(默认)` 的值为 <启动命令>，例如：

```powershell
"C:\Program Files\Neovim\bin\nvim-qt.exe" "%1"
```

### 4. 设置图标

在 `Open with neovim` 下新建 `可扩充字符串值` 项，命名为 `Icon`。

在右侧窗口中修改 `(默认)` 的值为 <图标或可执行文件的路径>，例如：

```powershell
C:\Program Files\Neovim\bin\nvim-qt.exe
```

## 二、右键打开文件夹

定位到 `HKEY_CLASSES_ROOT\Directory\shell` 分支，然后参照上述步骤即可。

## 三、右键空白处，打开当前文件夹

定位到 `HKEY_CLASSES_ROOT\Directory\Background\shell\` 分支，参照上述步骤执行，但是需要注意：

在步骤 3 中，把 `%1` 改为 `%V`，例如：

```powershell
"C:\Program Files\Neovim\bin\nvim-qt.exe" "%V"
```
