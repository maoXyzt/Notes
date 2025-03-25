# 用 Nuitka 编译 python 代码

本文运行环境：

+ Windows 10
+ python 3.10
+ nuitka == 2.5.8

## 1 - 环境配置

### 1.1 Requirements

+ C Compiler
+ python
+ Operating System
+ Architecture

#### 1.1.1 C 编译器

nuitka 打包需要支持 C11 的 C 环境。

Windows 平台可以使用如下编译器:

+ **Visual Studio 2022** 或者更高版本: 建议使用默认的 English language pack。
  + 通过 `--msvc=latest` 参数强制使用 Visual Studio。
+ **MinGW64**: 必须使用由 Nuitka 下载的版本。
  + 如果 Nuitka 没有找到 Visual Studio，将会建议下载 MinGW64。通过 `--mingw64` 参数可以强制使用 MinGW64。
+ **Clang-cl**: 如果 Visual Studio 提供了 Clang-cl 编译器，则也可以使用通过 `--clang` 参数使用。
+ **Clang**: 如果 MingGW64 提供了 Clang 编译器，则也可以使用通过 `--mingw64 --clang` 参数使用。

Linux 平台使用系统的 GCC 编译器或安装的 clang 编译器。

macOS 平台使用系统的 Clang 编译器。(需要安装 XCode)

> 更多平台支持，参考 [Nuitka User Manual#C Compiler](https://nuitka.net/user-documentation/user-manual.html#c-compiler)

#### 1.1.2 Python

Nuitka 目前支持 Python >= 3.4 和 Python 2.6, 2.7。

如果使用的并非当前活跃的 Python 版本(3.9--3.13)，查看文档检查是否有什么注意事项。[Nuitka User Manual#Python](https://nuitka.net/user-documentation/user-manual.html#python)

```bash
pip install nuitka==2.5.8
```

注意：

+ 如果希望生成的二进制文件可以在其他机器上运行，需要使用 `--mode=standalone`, `--mode=onefile` 或者 `--mode=app` 参数。不能使用 `--mode=accelerated` 参数。
+ 文件后缀:
  + Windows 平台生成的文件后缀为 `.exe`
  + 其他平台在 `--mode=standalone` 时无后缀，否则后缀为 `.bin`。 可通过 `--output-filename` 改变。
  + 在 `--mode=onefile` 和 `--mode=accelerated` 时，Nuitka 会自动添加 `.bin` 后缀。
+ Module mode 下的文件名: 不能直接重命名生成的 module 文件，filename 和 module name 必须一致。只能通过重命名源文件来改变。
+ 只能使用标准的 Python 实现（CPython）
  + 支持 Anaconda Python
  + 支持 Homebrew Python 的支持，但跨机器和向后兼容的效果不那么理想。
  + 不支持通过 Microsoft Store 安装的 Python。
  + 不支持 macOS pyenv。建议使用 Homebrew 版本。

#### 1.1.3 操作系统

Nuitka 支持的操作系统: Android, Linux, FreeBSD, NetBSD, OpenBSD, macOS, Windows (32bits/64 bits/ARM)。

其他操作系统也可以使用，但需要调整 Nuitka 的内部 SCons 用法，或提供额外的 flag。

确保 Python 版本与 C 编译器的架构一致，否则将会出现晦涩难懂的错误信息。

#### 1.1.4 架构

Nuitka 支持的架构: x86, x86_64 (AMD64), ARM。

其他架构也可以使用，通常 **Debian** 或 **RHEL** 支持的架构都可以使用。

### 1.2 安装

> [Nuitka Downloads](https://nuitka.net/doc/download.html)

```bash
pip install nuitka==2.5.8
```

## 2 - 编译

```shell
python -m nuitka
```

### 2.1 编译选项 Options

可以在文件开头添加如下注释，指定编译选项

```python
# Compilation mode, support OS-specific options
# nuitka-project-if: {OS} in ("Windows", "Linux", "Darwin", "FreeBSD"):
#    nuitka-project: --onefile
# nuitka-project-else:
#    nuitka-project: --mode=standalonealone

# The PySide6 plugin covers qt-plugins
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-qt-plugins=qml
```

支持预设变量展开，参照 [Nuitka User Manual#Nuitka Project Options](https://nuitka.net/user-documentation/user-manual.html#nuitka-project-options)

#### 2.1.1 数据文件

(1) 通过 `--include-package-data=package_name` 参数指定 package 需要包含的数据文件。

Examples:

+ `--include-package-data=package_name` (all files)
+ `--include-package-data=package_name:*.txt` (only certain type)
+ `--include-package-data=package_name:some_filename.dat` (concrete file)

(2) 通过 `--include-data-files` 匹配数据文件的文件名。

参数中可以使用变量，如 `{MAIN_DIRECTORY}`。

Examples:

+ `--include-data-files=/path/to/file/some.txt=folder_name/some.txt` 拷贝单个文件。
+ `--include-data-files=/path/to/file/*.txt=folder_name/some.txt` 拷贝单个文件，如果匹配上了多个文件将会报错。
+ `--include-data-files=/path/to/files/*.txt=folder_name/` 将匹配的文件拷贝到目录中。
+ `--include-data-files=/path/to/scan=folder_name=**/*.txt` 保持目录结构递归拷贝匹配路径的内容。

(3) 通过 `--include-data-dir=DIRECTORY` 匹配目录。

将会递归拷贝目录下的所有文件。

+ 非递归包含，使用 `--include-data-files`
+ 包含整个目录，使用 `--include-data-dir=/path/some_dir=data/some_dir`
+ 使用 `--noinclude-data-files` 来移除匹配的文件

(4) 通过 `--include-onefile-external-data=PATTERN` 将数据文件打包的 onefile 之外。

将数据文件打包到 onefile binary 之外而不是 onefile 内。只在 `--onefile` 编译模式下有效。

需要先用上述方法包括数据文件，然后用 `--include-onefile-external-data` 指定 onefile 旁的路径。

#### 2.1.2 Tweaks

(1) Icons

<https://nuitka.net/user-documentation/user-manual.html#icons>

Example on Windows:

```shell
python -m nuitka --onefile --windows-icon-from-ico=your-icon.png program.py
python -m nuitka --onefile --windows-icon-from-ico=your-icon.ico program.py
python -m nuitka --onefile --windows-icon-template-exe=your-icon.ico program.py
```

Example on macOS:

```shell
python -m nuitka --macos-create-app-bundle --macos-app-icon=your-icon.png program.py
python -m nuitka --macos-create-app-bundle --macos-app-icon=your-icon.icns program.py
```

#### 2.1.3 MacOS Entitlements

<https://nuitka.net/user-documentation/user-manual.html#macos-entitlements>

#### 2.1.4 Windows UAC Configuration

<https://nuitka.net/user-documentation/user-manual.html#windows-uac-configuration>

#### 2.1.5 Console Window

在 Windows 平台，默认会打开一个 console 窗口。用 `--disable-console` 参数禁用。

用 `--enable-console` 参数强制打开。

## 3 - Examples

### 3.1 编译 module

```bash
# 编译单个文件
python -m nuitka --assume-yes-for-downloads --module --output-dir=build module.py
# 编译 module 文件夹
cd /path/to/module_parent_folder # ! 重要。否则无法 include package
python -m nuitka --assume-yes-for-downloads --module --output-dir=build module_folder --include-package=module_folder
```

## 4 - 交叉编译

> <https://github.com/Nuitka/Nuitka/issues/43#issuecomment-2100416081>
