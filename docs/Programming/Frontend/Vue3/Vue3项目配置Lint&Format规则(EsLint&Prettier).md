# Vue3 项目配置 Lint & Format 规则 (EsLint & Prettier)

## 1. 依赖

Vue3 项目初始化时，通过交互式选项已经自动安装了 Eslint 和 Prettier。

> [Vue3项目Setup](./Vue3项目Setup.md)

`package.json`:

```json
{
  "devDependencies": {
    "@vue/eslint-config-prettier": "^10.2.0",
    "@vue/eslint-config-typescript": "^14.4.0",
    "eslint": "^9.20.1",
    "eslint-plugin-vue": "^9.32.0",
    "prettier": "^3.5.1",
  }
}
```

## 2. Prettier 配置

配置文件 `.prettierrc.json5`:

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

## 3. ESLint 配置

配置文件 `eslint.config.ts`

```typescript

```
