# Notes

Personal notes

Powered by [vitepress](https://vitepress.vuejs.org/).

## Setup

```bash
poetry install
```

## Development

vitepress config: `docs/.vitepress/config.mts`

```bash
pnpm install
```

### 1) Build

Manually build the site:

```bash
pnpm docs:build
```

### 2) Preview

```bash
pnpm docs:preview
```

### 3) Commit 前

更新文档目录: `docs/toc.md` 文件和 `docs/structure.json` 文件

```bash
python -m cli.update_toc
```
