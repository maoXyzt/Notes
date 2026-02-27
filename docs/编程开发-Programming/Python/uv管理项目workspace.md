---
NoteStatus: Draft
---

# uv 管理项目 workspace

uv 支持类似 cargo workspace 模式的项目管理，可以实现多模块的开发机制。

workspace 的概念来自 `cargo`。

workspace 是多个项目集合，每个项目有自己的 `pyproject.toml` 文件，但只有一个 `uv.lock` 文件, 这保证了 workspace 中的依赖不会冲突。

workspace 的 member 可以是 application 或 library:

- [applications](https://docs.astral.sh/uv/concepts/projects/init/#applications) 适用于 web 服务、脚本、CLI 等项目
  - 这是 `uv init` 默认创建的项目类型
  - 建议加上 `--package` 选项， 使得它可以被构建为一个 package 被其他 member 引用
- [libraries](https://docs.astral.sh/uv/concepts/projects/init/#libraries) 是 Python 库，专用于被其他项目引用

## 1 - 创建 workspace

```bash
uv init --workspace
mkdir packages
```

把 `packages` 目录作为 workspace 的 member 目录。

```toml
# pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]
```

## 2 - 添加 member

```bash
# library
uv init --library packages/example-member-lib
# packaged application (省略了 `--application`)
uv init --package packages/example-member-app
```

在 `pyproject.toml` 中添加成员:

```toml
# pyproject.toml
[tool.uv.sources]
example-member-lib = { workspace = true }
example-member-app = { workspace = true }
```

项目中代码和 member 的代码中，可以相互引用:

```python
from example_member_lib import some_function
from example_member_app import some_app
```
