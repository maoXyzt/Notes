---
type: note
aliases: []
created: 2025-09-11T15:39:00.000+0800
modified: 2026-10-20T02:26:18.000+0800
tags: []
---

# Obsidian 插件推荐

## 1 - 插件一览

本页按功能和使用需求推荐插件，推荐级别不代表本库当前启用状态。当前库启用 21 个插件，完整名单见主仓库 `dotfiles/README.md`。

+ [Advanced Tables](https://github.com/tgrosinger/advanced-tables-obsidian)
+ [Better Search Views](https://github.com/ivan-lednev/better-search-views)
+ [Calendar Plus](https://github.com/mattmaiorana/calendar-plus)
+ [Commander](https://github.com/phibr0/obsidian-commander)
+ [Copilot](https://github.com/logancyang/obsidian-copilot)
+ [Dataview](https://github.com/blacksmithgu/obsidian-dataview)
+ [Editing Toolbar](https://github.com/cumany/obsidian-editing-toolbar)
+ [Export to Anki](https://github.com/Pseudonium/Obsidian_to_Anki)
+ [File Explorer Note Count](https://github.com/ozntel/file-explorer-note-count)
+ [Floating TOC](https://github.com/PKM-er/obsidian-floating-toc-plugin)
+ [Fuzzy Chinese Pinyin](https://github.com/lazyloong/obsidian-fuzzy-chinese)
+ [Hider](https://github.com/kepano/obsidian-hider)
+ [Homepage](https://github.com/mirnovov/obsidian-homepage)
+ [Iconize](https://github.com/FlorianWoelki/obsidian-iconize)
+ [Influx](https://github.com/jensmtg/influx)
+ [Keyboard Analyzer](https://github.com/cogscides/obsidian-keyboard-analyzer)
+ [Linter](https://github.com/platers/obsidian-linter)
+ [Meta Bind](https://github.com/mProjectsCode/obsidian-meta-bind-plugin)
+ [Metadata Menu](https://github.com/mdelobelle/metadatamenu)
+ [Natural Language Dates](https://github.com/community-archive/nldates)
+ [Omnisearch](https://github.com/scambier/obsidian-omnisearch)
+ [Open vault in VS Code](https://github.com/NomarCub/obsidian-open-vscode)
+ [Outliner](https://github.com/vslinko/obsidian-outliner)
+ [QuickAdd](https://github.com/chhoumann/quickadd)
+ [Recent Files](https://github.com/tgrosinger/recent-files-obsidian)
+ [Self-hosted LiveSync](https://github.com/vrtmrz/obsidian-livesync)
+ [Sort & Permute lines](https://github.com/Vinzent03/obsidian-sort-and-permute-lines)
+ [Style Settings](https://github.com/mgmeyers/obsidian-style-settings)
+ [Tag Wrangler](https://github.com/pjeby/tag-wrangler)
+ [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks)
+ [Templater](https://github.com/SilentVoid13/Templater)

## 2 - 分类推荐

⭐: 强烈推荐安装
👍: 提升使用体验，建议安装
🉑: 按需安装

## 2.1 功能性增强

+ ⭐ Dataview: 实现强大的数据查询和展示功能
+ ⭐ Templater: 高级模板
+ ⭐ Tasks: 任务管理
+ ⭐ Calendar Plus: 显示日历，点击日期可创建/打开对应日期的日记；内置日记、周记、月记、季记和年记功能。各类周期笔记的目录、日期格式和模板需在插件内独立配置，不读取核心 Daily Notes 或 Periodic Notes 的设置；当前库仅启用日记。
+ ⭐ QuickAdd: 快速创建/插入内容，支持 Template, Capture, Macro
+ ⭐ Tag Wrangler: 在 Tags View (核心插件) 中，添加 tag 的右键菜单，实现 tag 重命名、搜索、创建 Tag Page 等功能
+ 🉑 Copilot: 接入 LLM API，使用 AI 助手
+ 👍 Self-hosted LiveSync: 同步 Obsidian 笔记到自托管 CouchDB 服务器 (见 [Obsidian 同步 - 配置 LiveSync 与自托管 CouchDB 服务器](./Obsidian%20同步%20-%20配置%20LiveSync%20与自托管%20CouchDB%20服务器.md))
+ 🉑 Commander: 配置一些快捷指令，可以放置在 TitleBar, Page Header, File Menu, Ribbons, Context Menu, Status Bar 等位置
+ 🉑 Export to Anki: 支持创建 Anki 卡片，并导出到 Anki
+ 🉑 Openvault in VS Code: 在 VS Code 中打开当前 vault
+ 👍 Omnisearch: 全文搜索增强，按文件名、标题和正文的相关性排序，支持拼写容错、库内和文件内搜索，以及从结果插入双链；图片、PDF 和 Office 文档的内容索引需配合 Text Extractor
+ 👍 Fuzzy Chinese Pinyin: 提供中文拼音搜索的功能，支持繁体、双拼、模糊音
+ 🉑 Keyboard Analyzer: 分析按键和快捷指令的使用频率，帮助优化快捷指令设置

## 2.2 Markdown 编辑增强

+ 👍 Advanced Tables: 增强表格编辑功能
+ 🉑 Outliner: 增强列表编辑功能，类似 Workflowy 和 Roam Research
+ 🉑 Editing Toolbar: 提供一个编辑工具栏
+ ⭐ Linter: markdown 格式化
+ 🉑 Natural Language Dates: 适合频繁在正文中通过 `@today`、`@tomorrow` 等自然语言插入日期及日记链接的用户；仅通过 Calendar Plus 打开、创建日记，或仅用 Templater 在模板中插入日期时，可不安装
+ 🉑 Meta Bind: 在笔记中插入输入控件、显示控件、按钮等元素，可把值绑定到笔记的 frontmatter 元数据中
+ 👍 Metadata Menu: 管理 frontmatter 元数据，增强元数据的编辑功能
+ 🉑 Sort & Permute lines: 对选中行进行排序、随机打乱等操作

## 2.3 UI 增强和个性化

+ 🉑 Homepage: 使得 Obsidian 启动时打开指定 homepage (note, canvas, base 或 workspace)
+ 👍 Style Settings: 自定义样式。很多主题和插件都支持用它来调整样式
+ 👍 Iconize: 设置目录、文件的自定义图标
+ 🉑 Hider: 隐藏 Obsidian UI 的一些元素
+ 🉑 Recent Files: 显示最近打开的文件列表
+ 🉑 File Explorer Note Count: 在文件资源管理器中显示每个文件夹中的笔记数量
+ 🉑 Floating TOC: 鼠标悬停时，显示笔记的内容
+ 👍 Better Search Views: 增强搜索结果的显示
+ 🉑 Influx: 在笔记中显示该笔记的反向链接
