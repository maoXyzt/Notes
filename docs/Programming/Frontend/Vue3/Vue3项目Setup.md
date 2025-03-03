# Vue3 项目 Setup

## 1. 安装 Vue3

[Creating a Vue Application](https://vuejs.org/guide/quick-start.html#creating-a-vue-application)

```bash
pnpm create vue@latest
```

根据提示选择配置项，完成项目初始化。

* 启用 TypeScript
* 启用 Vue Router
* 启用 Pania
* 启用 ESLint
* 启用 Prettier

## 2 安装推荐的依赖

### 2.1 vue-query: 数据请求和缓存

pinia 用于处理公共状态，vue-query 用于处理服务端状态。

[TanStack Query](https://tanstack.com/query/latest/docs/framework/vue/overview)

```bash
pnpm add @tanstack/vue-query
```

### 2.2 VueUse

一些常用的 Vue Composition API 钩子函数。

```bash
pnpm i @vueuse/core
```

### 2.3 tiny-invariant

用于检查条件是否满足，不满足则抛出异常。可以消除 typescript 中的一些警告。

<https://www.npmjs.com/package/tiny-invariant>

```bash
pnpm i tiny-invariant
```

### 2.4 其他

* axios: 网络请求
* cross-env: 跨平台环境变量
* generate-changelog: 生成 `CHANGELOG.md`

```bash
pnpm i axios
pnpm i -D cross-env
pnpm i -D generate-changelog
```

## 3. 安装组件库

### 3.1 Naive UI

```bash
pnpm i -D naive-ui
pnpm i -D vfonts  # 字体
```

配置按需引入组件:

> 见 [4. 安装推荐插件](#4-安装推荐插件)

## 4. 安装推荐插件

### 4.1 Vite 插件

[自动按需引入组件](./Vue3自动按需引入组件(unplugin-vue-components).md)

### 4.2 UnoCSS

[UnoCSS](./Vue3%20UnoCSS安装和配置.md)

### 4.3 CSS 预处理器 (PostCSS)

> <https://cn.vite.dev/guide/features#postcss>

```bash
pnpm add -D postcss-loader postcss
# `postcss-nesting` 支持 W3C 标准的 CSS嵌套;
# 如果希望使用 sass 风格的嵌套，则选择 `postcss-nested`
pnpm add -D postcss-nesting
```

配置 `vite.config.ts` 的 css 配置项:

```typescript
import postcssNesting from 'postcss-nesting'

export default defineConfig({
  css: {
    postcss: {
      plugins: [postcssNesting()],
    },
  },
  // ...
})
```

## 5. 项目配置

### 5.1 配置项目 Node.js 版本

用于 [fnm](https://github.com/Schniz/fnm?tab=readme-ov-file) 管理 Node.js 版本。

创建 `.node-version` 文件，内容为项目所需的 Node.js 版本。

```bash
echo "22.14.0" > .node-version
```

### 5.2 配置代码规范 (Eslint & Prettier)

基于 Eslint 和 Prettier 配置的代码规范。

见 [Vue3 项目配置 Lint & Format 规则 (EsLint & Prettier)](./Vue3项目配置Lint&Format规则(EsLint&Prettier).md)

### 5.3 配置 Pre-commit Hook

使用 [Husky](https://typicode.github.io/husky/) 配置 pre-commit hook，用于在提交代码前执行代码检查。

```bash
pnpm i -D husky
pnpm exec husky install
```

配置见: [Husky-配置前端项目的 git hooks](../Husky-配置前端项目的git%20hooks.md)

### 5.4 项目 vite 配置

见 [Vue3 项目 Vite 配置](./Vue3项目Vite配置.md)
