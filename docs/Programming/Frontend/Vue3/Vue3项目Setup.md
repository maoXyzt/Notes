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

## 2 安装依赖

### sass

```bash
pnpm install sass sass-loader --save-dev
```

### vue-query: 数据请求和缓存

pinia 用于处理公共状态，vue-query 用于处理服务端状态

[TanStack Query](https://tanstack.com/query/latest/docs/framework/vue/overview)

```bash
pnpm add @tanstack/vue-query
```

### VueUse

```bash
pnpm i @vueuse/core
```

### tiny-invariant

<https://www.npmjs.com/package/tiny-invariant>

```bash
pnpm i tiny-invariant
```

### naive-ui

```bash
pnpm i -D naive-ui
pnpm i -D vfonts  # 字体
```

## 3. 配置

### 3.1 配置 Prettier

配置文件 `.prettierrc.json5`

```json5
{
  $schema: 'https://json.schemastore.org/prettierrc',
  // 不尾随分号
  semi: false,
  // 使用双引号
  singleQuote: true,
  // 一行最多 xx 字符
  printWidth: 100,
  // 对象大括号内两边是否加空格 { a:0 }
  bracketSpacing: true,
  // 单个参数的箭头函数加括号 (x) => x
  arrowParens: 'always',
  bracketSameLine: false,
  endOfLine: 'lf',
  jsxBracketSameLine: false,
  jsxSingleQuote: false,
  // 使用 2 个空格缩进
  tabWidth: 2,
  // 多行逗号分割的语法中，最后一行加逗号
  trailingComma: 'all',
  // 不使用缩进符，而使用空格
  useTabs: false,
  vueIndentScriptAndStyle: false,
  embeddedLanguageFormatting: 'off',
}
```

### 3.2 配置 ESLint

### 3.3 配置 Pre-commit Hook

### 3.4 创建 `.node-version` 文件

用于 [fnm](https://github.com/Schniz/fnm?tab=readme-ov-file) 管理 Node.js 版本。

```bash
20.14.0
```

## 4. 插件

* [自动按需引入组件](./Vue3自动按需引入组件(unplugi-vue-components).md)
* [UnoCSS](./Vue3%20UnoCSS安装和配置.md)
