---
NoteStatus: draft
---

# uv 使用教程

[uv](https://github.com/astral-sh/uv) 是 Python 的包管理工具，出自 [ruff](https://github.com/astral-sh/ruff) 项目相同的作者。拥有如下亮点:

- 🚀 一个工具替代 `pip`、`pip-tools`、`pipx`、`poetry`、`pyenv`、`twine`、`virtualenv` 等多个工具
- ⚡️ 比 `pip` 快 10-100 倍
- 🗂️ 提供全面的项目管理，使用通用的 lockfile
- ❇️ 运行脚本，支持 inline dependencies metadata
- 🐍 安装和管理 Python 版本
- 🛠️ 运行和安装以 Python Package 形式发布的工具
- 🔩 包含与 `pip` 兼容的接口，在保持熟悉 CLI 的同时提升性能
- 🏢 支持 Cargo 风格的 workspace，适用于可扩展项目
- 💾 节约磁盘空间，使用全局缓存进行依赖去重

## 1 - 安装

### 1.1 - 安装方法

> 官方安装文档: [Installation methods](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

使用官方脚本安装:

```bash
# Linux & macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

用各种包管理器安装:

```bash
# Homebrew (macOS)
brew install uv
# winget (Windows)
winget install --id=astral-sh.uv  -e
# scoop (Windows)
scoop install main/uv
```

用 cargo 源码编译安装:

```bash
cargo install --git https://github.com/astral-sh/uv uv
```

### 1.2 - 更新 uv

```bash
uv self update
```

### 1.3 - 卸载 uv

#### 1.3.1 - 清除下载的数据

```bash
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
```

#### 1.3.2 - 删除 `uv` 和 `uvx` 可执行文件

不确定安装方式时，可以先用 `which uv` 或者 `Get-Command uv` 查看安装位置再判断。

(1) 使用官方脚本安装的情况下，直接移除 `uv` 和 `uvx` 可执行文件:

```bash
# Linux & macOS
rm ~/.local/bin/uv ~/.local/bin/uvx
```

(2) 使用包管理器安装的情况下:

```bash
# Homebrew
brew uninstall uv
# winget
winget uninstall uv
# scoop
scoop uninstall uv
```

(3) 使用 cargo 源码编译安装的情况下:

```bash
rm ~/.cargo/bin/uv"
```

## 2 - 基本使用

### 2.1 - 创建项目: `uv init`

```bash
uv init [OPTIONS] [PATH]
```

会创建 `pyproject.toml` 文件，并创建一个默认的 `src` 目录, `main.py` 文件, `.python-version` 文件, `README.md` 文件等。
如果目标的任何一级上级目录存在 `pyproject.toml` 文件, 则会将新建的项目添加为 workspace 中的一个 member (除非指定了 `--no-workspace` 选项)。

PATH 参数:

- 新项目的位置: 默认为当前目录

OPTIONS 部分有用的选项:

- `--python`: 指定 Python 版本。例如: `--python=3.12`
- `--bare`: 只创建 `pyproject.toml` 文件
- `--build-backend`: 指定 build backend。常用值: `--build-backend=hatchling`
- `--lib`: 创建一个 library 项目 (此类项目专用于作为 package 被其他项目引用)
- `--script`: 创建一个 script。它是一个单独的脚本文件，符合 [PEP 723](https://peps.python.org/pep-0723/) 标准。它的依赖会被安装到当前 python 的依赖中。
- `-v`: 显示详细信息

Examples:

```bash
# 创建一个 library 项目
uv init --lib mylib --build-backend=hatchling
# 创建一个 script
uv init --script myscript.py
# 创建一个项目
uv init myproject --build-backend=hatchling --python=3.12
```

## 3 - Example

可从 airflow 项目的 `pyproject.toml` 文件学习大型项目的 uv 配置:

<https://github.com/apache/airflow/blob/main/pyproject.toml>
