---
NoteStatus: draft
---

# uv 管理项目 workspace

uv 支持类似 cargo workspace 模式的项目管理，可以实现多模块的开发机制。

workspace 的概念来自 `cargo`。

workspace 是多个项目集合，每个项目有自己的 `pyproject.toml` 文件，但只有一个 `uv.lock` 文件, 这保证了 workspace 中的依赖不会冲突。

workspace 的 member 可以是 application 或 library:

- [applications](https://docs.astral.sh/uv/concepts/projects/init/#applications) 适用于 web 服务、脚本、CLI 等项目
  - 这是 `uv init` 默认创建的项目类型
- [libraries](https://docs.astral.sh/uv/concepts/projects/init/#libraries) 是 Python 库，专用于被其他项目引用

## 1 - 创建 workspace

```bash
uv init --workspace
```
