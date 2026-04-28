# 笔记

个人笔记

基于 [vitepress](https://vitepress.vuejs.org/) 框架构建。

## 目录结构

```text
.
├── cli/                    # 命令行工具与脚本
├── docs/
│   ├── .vitepress/         # VitePress 配置目录
│   ├── index.md            # 站点首页
│   ├── toc.md              # 文档目录索引
│   └── ...                 # 其余 markdown 均为笔记文档
├── AGENTS.md               # 项目约定说明
├── package.json            # Node.js / VitePress 脚本配置
├── pyproject.toml          # Python 项目配置
├── uv.lock                 # Python 依赖锁定文件
├── pnpm-lock.yaml          # Node.js 依赖锁定文件
└── README.md               # 项目说明
```

### docs/.vitepress 目录说明

- `docs/.vitepress/config.mts`：VitePress 主配置入口，汇总文档配置、主题配置、`head` 配置，并启用 MathJax 数学公式渲染。
- `docs/.vitepress/constants.ts`：站点常量配置（如 `base_url`、站点标题、GitHub 地址）。
- `docs/.vitepress/docs.ts`：文档站点基础配置（语言、描述、lastUpdated、路由等）。
- `docs/.vitepress/head.ts`：页面 `head` 配置（如 favicon、统计脚本）。
- `docs/.vitepress/theme/`：主题相关配置与样式目录。

### cli 工具说明

- `cli/update_toc.py`：扫描 `docs/` 目录并生成/更新 `docs/structure.json` 与 `docs/toc.md`（忽略 `index.md`、`toc.md` 与草稿文档）。
- `cli/utils/structure.py`：定义目录结构模型（分组/页面）与构建逻辑，负责解析 markdown、提取标题、排序并组织层级结构。
- `cli/utils/tools.py`：通用工具函数（如链接转义、提取 markdown 一级标题）。
- `cli/utils/constants.py`：CLI 相关常量定义（如笔记状态枚举）。
- `cli/__init__.py`、`cli/utils/__init__.py`：包初始化文件（用于模块组织与导入）。

## 环境准备

```bash
uv sync --all-extras
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
uv run update-toc
```
