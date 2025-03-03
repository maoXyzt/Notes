# VitePress 插件

[[toc]]

## 1. 评论区

> Ref: <https://vitepress.yiov.top/plugin.html#%E8%AF%84%E8%AE%BA>

使用 [giscus](https://github.com/apps/giscus) 实现评论区功能。

giscus 是一个基于 GitHub Discussion 的评论系统。它将评论数据都放在 GitHub 仓库的 Discussions 中。

> GitHub登录后方可评论，评论数据在 GitHub Discussions 中，评论后有邮件通知，无需部署服务端，UI爱了

### 1.1 安装 giscus

进 giscus App 官网：<https://github.com/apps/giscus>，点击 `Install` 安装。

选择 `Only select repositories`，再指定一个你想开启讨论的仓库。该仓库必需是公开的。也可以单独创建一个仓库用于评论。

### 1.2 生成数据

我们进入要开启讨论的仓库，点 "Settings"，在 Features 中勾选 "Discussions"。

进入官网：<https://giscus.app/zh-CN>

在 `配置 -> 仓库` 中输入自己的仓库链接，满足条件会提示可用。

下拉到 `Discussion 分类` 我们按推荐的选 "Announcements"。

`特性` 中的 "懒加载评论" 也可以勾选下。

下方的 `启用 giscus` 中会生成一个代码片段。示例如下:

我们需要关注其中 `data-repo`、 `data-repo-id`、 `data-category` 和 `data-category-id` 是关键数据。)

```html
<script src="https://giscus.app/client.js"
        data-repo="****/****"
        data-repo-id="**************"
        data-category="Announcements"
        data-category-id="**************"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
```

### 1.3 在页面中使用

使用 [vitepress-plugin-comment-with-giscus](https://github.com/T-miracle/vitepress-plugin-comment-with-giscus) 插件，实现页面中的评论区。

```bash
pnpm add -D vitepress-plugin-comment-with-giscus
```

在 `.vitepress/theme/index.ts` 中填入下面代码:

```typescript
import giscusTalk from 'vitepress-plugin-comment-with-giscus';
import { useData, useRoute } from 'vitepress';

export default {
  // ...
  setup() {
    // Get frontmatter and route
    const { frontmatter } = useData();
    const route = useRoute();

    // giscus配置
    giscusTalk({
      repo: 'your github repository', //仓库
      repoId: 'your repository id', //仓库ID
      category: 'Announcements', // 讨论分类
      categoryId: 'your category id', //讨论分类ID
      mapping: 'pathname',
      inputPosition: 'bottom',
      lang: 'zh-CN',
      },
      {
        frontmatter, route
      },
      //默认值为true，表示已启用，此参数可以忽略；
      //如果为false，则表示未启用
      //您可以使用“comment:true”序言在页面上单独启用它
      true
    );

    // ...
  },
  // ...
}
```

#### 关闭评论区

我们可以在当前页使用 Frontmatter 关闭评论区，如下:

```yaml
---
comment: false
---
```
