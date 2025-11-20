# 笔记

个人笔记

基于 [vitepress](https://vitepress.vuejs.org/) 框架构建。

## 环境准备

```bash
uv venv
uv sync --dev
pre-commit install
```

## 开发

vitepress 配置：`docs/.vitepress/config.mts`

```bash
pnpm install
```

### 1) 构建

手动构建站点（用于检查断链等）：

```bash
pnpm docs:build
```

### 2) 预览

```bash
pnpm docs:preview
```

### 3) 提交前

更新文档目录：`docs/toc.md` 文件和 `docs/structure.json` 文件

```bash
poetry run update-toc
```
