# Poetry 的基本使用

> [Poetry](https://python-poetry.org/)

## 0 - Why Poetry

Poetry 相对于 pip 有以下几个主要优点：

+ 依赖解析：Poetry 拥有一个内置的依赖解析器，可以自动解析项目的依赖关系，确保安装的包版本之间没有冲突。这与 pip 使用的 `requirements.txt` 不同，后者需要手动管理和指定每个包的版本。
+ 锁定文件：Poetry 使用 `poetry.lock` 文件锁定依赖项的版本，确保项目在不同环境中的一致性和可重现性。这意味着在其他环境中安装依赖项时，Poetry 会确保使用与锁定文件中记录的相同版本。
+ 环境隔离：Poetry 支持自动创建和管理虚拟环境，从而确保项目的依赖项与系统全局安装的包隔离。这有助于避免因全局包版本冲突而导致的问题。
+ 项目配置：Poetry 使用 `pyproject.toml` 文件统一管理项目配置和依赖关系，使得项目结构更加清晰和易于维护
+ 包发布：Poetry 提供了一种简单的方法来构建和发布 Python 包，它可以自动生成 `setup.py`、`setup.cfg` 和 `MANIFEST.in` 等文件，从而简化了发布过程
+ 简化的命令行界面：Poetry 提供了一个简洁、统一的命令行界面，用于管理项目的依赖关系、虚拟环境和包发布。与 `requirements.txt` 相比，这使得依赖管理更加直观和一致。
+ 一致的软件包安装：Poetry 为安装任何软件包提供一致的格式，确保整个项目采用标准化的方法
+ 广泛的软件包选择：Poetry 提供了对 PyPI 上广泛软件包的访问，使你可以为你的项目利用一个多样化的生态系统
+ 高效的依赖性管理：Poetry 只为指定的软件包安装必要的依赖性，减少环境中不相干的软件包的数量
+ 简化的软件包移除：Poetry 简化了软件包及其相关依赖关系的移除，使其易于维护一个干净和高效的项目环境

## 1 - 安装 Poetry

> <https://python-poetry.org/docs/#installing-with-pipx>

安装：

```bash
pipx install poetry
```

更新、卸载：

```bash
pipx upgrade poetry
pipx uninstall poetry
```

命令行补全

```bash
# For bash
poetry completions bash >> ~/.bash_completion
```

```bash
# For oh-my-zsh
mkdir $ZSH_CUSTOM/plugins/poetry
poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry

# Enable the plugin in `~/.zshrc`
# plugins(
#   poetry
#   ...
# )
```

## 2 - 项目管理

### 创建项目

```bash
poetry new my-project
```

### Python 版本管理

在 `pyproject.toml` 中指定 Python 版本 (支持的最小版本为 3.7.0):

```toml
[tool.poetry.dependencies]
python = "^3.7.0"
```

### 在已有项目中初始化 poetry

```bash
poetry init
```

### 运行模式

默认为 package 模式。

+ 当前项目是一个 package
+ 可以用 `poetry publish` 命令打包和发布 package
+ `pyproject.toml` 中的 `name` 和 `version` 必须指定

非 package 模式时，poetry 仅用来管理依赖。

```toml
[tool.poetry]
package-mode = false
```

## 3 - 依赖管理

### 在 `pyproject.toml` 中指定依赖

```bash
[tool.poetry.dependencies]
pendulum = "^2.1"
```

### 命令添加依赖

```bash
poetry add pendulum
```

### 安装依赖

```bash
# package 模式 (默认) 时，会以 editable (-e) 模式安装当前项目
poetry install
# 仅安装依赖
poetry install --no-root
```

升级依赖 (会无视 `poetry.lock` 文件):

```bash
poetry update
```

## 4 - 虚拟环境

默认情况下，poetry 会创建虚拟环境到 `{cache-dir}/virtualenvs` 目录下。

> `cache-dir` 可通过 poetry configuration 配置

如果使用并激活了其他虚拟环境，则 poetry 会使用该虚拟环境。

通过 `poetry shell` 命令可以创建一个使用新的虚拟环境的 shell。

+ 通过 `exit` 命令可以退出该 shell。
+ 通过 `deactivate` 命令可以退出虚拟环境但保留 shell。

如果不想创建 shell, 则通过 `source {path_to_venv}/bin/activate` 手动激活虚拟环境。

+ `{path_to_venv}\Scripts\activate.ps1` in PowerShell
+ `poetry env info --path` 查看虚拟环境路径
  + 一行命令激活: `source $(poetry env info --path)/bin/activate`
+ 通过 `deactivate` 命令退出虚拟环境

## 5 - 运行脚本与命令

```bash
poetry run python my-script.py
poetry run pytest
poetry run ruff check .
```

如果使用并激活了其他虚拟环境，则不需要使用 `poetry run` 命令，直接使用 `python my-script.py` 即可。

## 6 - 与 pre-commit 集成

poetry 提供了如下 pre-commit hooks:

### 6.1 poetry-check

`poetry-check` hook 执行 `poetry check` 命令，确保 poetry 配置不会以损坏的状态提交。

### 6.2 poetry-lock

`poetry-lock` hook 执行 `poetry lock` 命令，确保 `poetry.lock` 文件是最新的。

### 6.3 poetry-export

`poetry-export` hook 执行 `poetry export` 命令，将依赖项导出到指定文件中。

#### 6.3.1 安装插件

"poetry>=2.0"版本默认不含 export 命令，需要安装插件 [Poetry Plugin: Export](https://github.com/python-poetry/poetry-plugin-export)。

安装方式:

```toml
# pyproject.toml
# requires poetry >= 2.0
[tool.poetry.requires-plugins]
poetry-plugin-export = ">=1.8"
```

命令行安装:

```bash
poetry self add poetry-plugin-export
# 如果 poetry 是通过 pipx 安装的
pipx inject poetry poetry-plugin-export
# 如果 poetry 是通过 pip 安装的
pip install poetry-plugin-export
```

#### 6.3.2 配置参数

默认使用如下参数（以 `requirements.txt` 格式输出到控制台）：

```yaml
# .pre-commit-config.yaml
hooks:
- id: poetry-export
  args: ["-f", "requirements.txt"]
```

可以通过 `args` 参数指定其他参数，如:

```yaml
# .pre-commit-config.yaml
hooks:
- id: poetry-export
  args: ["--with", "dev", "-f", "requirements.txt", "-o", "requirements.txt"]
  verbose: true
```

`verbose: true`: 同时将文件输出到控制台。

+ `--format` (`-f`): 导出格式 (默认: `requirements.txt`)。 目前只支持 `constraints.txt` 和 `requirements.txt` 格式。
+ `--output` (`-o`): 输出文件 (默认: 输出到 stdout)。
+ `--with`: 包含可选和非可选的依赖组。默认情况下，仅包含主要依赖项。
+ `--only`: 仅包含指定的依赖组。可以通过这种方式排除主要组。
+ `--extras` (`-E`): 包含指定的额外依赖项。
+ `--all-extras`: 包含所有额外依赖项。
+ `--all-groups`: 包含所有依赖组。
+ `--without-hashes`: 排除导出文件中的哈希。
+ `--with-credentials`: 包含额外索引的凭据。
