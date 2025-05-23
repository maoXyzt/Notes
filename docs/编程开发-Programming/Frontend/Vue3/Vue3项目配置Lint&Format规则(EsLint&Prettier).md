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

### eslint-config-prettier

关闭所有不必要的规则或可能与 Prettier 冲突的规则, 使 Prettier 能够格式化代码。

> [eslint-config-prettier](https://github.com/prettier/eslint-config-prettier):

安装:

```bash
pnpm add -D eslint-config-prettier
```

配置 `eslint.config.ts`:

```typescript
// import someConfig from "some-other-config-you-use";
import eslintConfigPrettier from "eslint-config-prettier";

export default [
  // someConfig,
  // ...
  eslintConfigPrettier,
];
```

### @stylistic/eslint-plugin

代码风格检查插件。

> [@stylistic/eslint-plugin](https://eslint.style/)

安装:

```bash
pnpm add -D @stylistic/eslint-plugin
```

配置 `eslint.config.ts`:

```typescript
import stylistic from '@stylistic/eslint-plugin'

export default [
  {
    plugins: {
      '@stylistic': stylistic,
      // other plugins
      // ...
    },
    rules: {
      /** ---- Stylistic ---- */
      /** 以下为我的个人配置, 可以根据项目实际要求取舍 */
      '@stylistic/indent': ['error', 2, { SwitchCase: 1 }],
      '@stylistic/linebreak-style': ['error', 'unix'],
      '@stylistic/quotes': ['error', 'single', { avoidEscape: true, allowTemplateLiterals: true }],
      '@stylistic/semi': ['error', 'never'],
      '@stylistic/comma-dangle': ['error', 'always-multiline'],
      '@stylistic/comma-spacing': ['error', { before: false, after: true }],
      '@stylistic/space-infix-ops': 'error',
      '@stylistic/arrow-spacing': 'error',
      '@stylistic/arrow-parens': ['error', 'always'], // 箭头函数参数括号
      '@stylistic/brace-style': ['error', '1tbs', { allowSingleLine: true }],
      '@stylistic/block-spacing': 'error',
      '@stylistic/computed-property-spacing': ['error', 'never'],
      '@stylistic/key-spacing': ['error', { beforeColon: false, afterColon: true }],
      '@stylistic/multiline-ternary': ['error', 'always-multiline'], // 多行三元表达式
      '@stylistic/no-mixed-spaces-and-tabs': 'error',
      '@stylistic/no-multi-spaces': ['error', { ignoreEOLComments: true }],
      '@stylistic/no-trailing-spaces': 'error',
      '@stylistic/object-curly-spacing': ['error', 'always'],
      '@stylistic/no-multiple-empty-lines': ['error', { max: 2, maxEOF: 1 }],
      '@stylistic/rest-spread-spacing': ['error', 'never'],
      '@stylistic/space-before-blocks': ['error', 'always'],
      '@stylistic/space-before-function-paren': [
        'error',
        {
          anonymous: 'always',
          named: 'never',
          asyncArrow: 'always',
        },
      ],
      '@stylistic/switch-colon-spacing': 'error',
      '@stylistic/template-curly-spacing': ['error', 'never'],
      '@stylistic/type-annotation-spacing': 'error',
      '@stylistic/type-generic-spacing': 'error',
      '@stylistic/type-named-tuple-spacing': 'error',
      // other rules
      // ...
    }
  }
]
```

### eslint-plugin-import

检查 import/export 语法。

> [eslint-plugin-import](https://github.com/import-js/eslint-plugin-import)

安装:

```bash
pnpm add -D eslint-plugin-import
```

配置 `eslint.config.ts`:

```typescript
import importPlugin from 'eslint-plugin-import'

export default [
  importPlugin.flatConfigs.recommended,
  importPlugin.flatConfigs.typescript,  // 当使用 typescript 时，必须引入
  {
    files: ['**/*.{js,mjs,cjs}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      /** ---- import ---- */
      /** 以下为我的个人配置, 可以根据项目实际要求取舍 */
      'import/order': [
        'error',
        {
          groups: [['builtin', 'external', 'internal'], ['parent', 'sibling', 'index'], 'type'],
          pathGroups: [
            {
              pattern: '@/assets/**',
              group: 'parent',
              position: 'before',
            },
            {
              pattern: '{@,.,..}/**/*.{vue,png,jpg,jpeg,gif,svg,css,scss,less,styl}',
              group: 'parent',
              position: 'before',
            },
            {
              pattern: '@/**',
              group: 'parent',
              position: 'before',
            },
            {
              pattern: '{.,..}/**/*.d.ts',
              group: 'type',
              position: 'after',
            },
          ],
          pathGroupsExcludedImportTypes: ['type'],
          alphabetize: {
            order: 'asc',
            caseInsensitive: true,
          },
          'newlines-between': 'always',
        },
      ],
    },
  },
]
```

### (可选) @unocss/eslint-config

UnoCSS 代码风格检查插件。

> [Vue UnoCSS安装和配置](./Vue3%20UnoCSS安装和配置.md)
> [UnoCSS ESLint Config](https://unocss.dev/integrations/eslint#eslint-config)

安装:

```bash
pnpm add -D @unocss/eslint-config
```

```typescript
import unocss from '@unocss/eslint-config/flat'

export default [
  // Other rules ...
  unocss,
]
```

### eslint 配置示例

`eslint.config.ts` 配置示例:

```typescript
// eslint.config.ts
import { includeIgnoreFile } from '@eslint/compat'
import stylistic from '@stylistic/eslint-plugin'
import unocss from '@unocss/eslint-config/flat'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'
import { defineConfigWithVueTs, vueTsConfigs } from '@vue/eslint-config-typescript'
import { globalIgnores } from 'eslint/config'
import importPlugin from 'eslint-plugin-import'
import pluginVue from 'eslint-plugin-vue'
import { fileURLToPath } from 'node:url'

const gitignorePath = fileURLToPath(new URL('.gitignore', import.meta.url))

// To allow more languages other than `ts` in `.vue` files, uncomment the following lines:
// import { configureVueProject } from '@vue/eslint-config-typescript'
// configureVueProject({ scriptLangs: ['ts', 'tsx'] })
// More info at https://github.com/vuejs/eslint-config-typescript/#advanced-setup

export default defineConfigWithVueTs(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },

  globalIgnores([
    '**/dist/**',
    '**/dist-ssr/**',
    '**/coverage/**',
    'src/lib/_client/**',
    'codegen/**',
    'node_modules/**',
  ]),
  includeIgnoreFile(gitignorePath),

  pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,
  skipFormatting,
  unocss,
  importPlugin.flatConfigs.recommended,
  importPlugin.flatConfigs.typescript,
  {
    plugins: {
      '@stylistic': stylistic,
      // other plugins
      // ...
    },
    rules: {
      /** ---- Stylistic ---- */
      '@stylistic/indent': ['error', 2, { SwitchCase: 1 }],
      '@stylistic/linebreak-style': ['error', 'unix'],
      '@stylistic/quotes': ['error', 'single', { avoidEscape: true, allowTemplateLiterals: true }],
      '@stylistic/semi': ['error', 'never'],
      '@stylistic/comma-dangle': ['error', 'always-multiline'],
      '@stylistic/comma-spacing': ['error', { before: false, after: true }],
      '@stylistic/space-infix-ops': 'error',
      '@stylistic/arrow-spacing': 'error',
      '@stylistic/arrow-parens': ['error', 'always'], // 箭头函数参数括号
      '@stylistic/brace-style': ['error', '1tbs', { allowSingleLine: true }],
      '@stylistic/block-spacing': 'error',
      '@stylistic/computed-property-spacing': ['error', 'never'],
      '@stylistic/key-spacing': ['error', { beforeColon: false, afterColon: true }],
      '@stylistic/multiline-ternary': ['error', 'always-multiline'], // 多行三元表达式
      '@stylistic/no-mixed-spaces-and-tabs': 'error',
      '@stylistic/no-multi-spaces': ['error', { ignoreEOLComments: true }],
      '@stylistic/no-trailing-spaces': 'error',
      '@stylistic/object-curly-spacing': ['error', 'always'],
      '@stylistic/no-multiple-empty-lines': ['error', { max: 2, maxEOF: 1 }],
      '@stylistic/rest-spread-spacing': ['error', 'never'],
      '@stylistic/space-before-blocks': ['error', 'always'],
      '@stylistic/space-before-function-paren': [
        'error',
        {
          anonymous: 'always',
          named: 'never',
          asyncArrow: 'always',
        },
      ],
      '@stylistic/switch-colon-spacing': 'error',
      '@stylistic/template-curly-spacing': ['error', 'never'],
      '@stylistic/type-annotation-spacing': 'error',
      '@stylistic/type-generic-spacing': 'error',
      '@stylistic/type-named-tuple-spacing': 'error',
      /** ---- import ---- */
      'import/no-unresolved': 0,
      'import/order': [
        'error',
        {
          groups: [['builtin', 'external', 'internal'], ['parent', 'sibling', 'index'], 'type'],
          pathGroups: [
            {
              pattern: '@/assets/**',
              group: 'parent',
              position: 'before',
            },
            {
              pattern: '{@,.,..}/**/*.{vue,png,jpg,jpeg,gif,svg,css,scss,less,styl}',
              group: 'parent',
              position: 'before',
            },
            {
              pattern: '@/**',
              group: 'parent',
              position: 'before',
            },
            {
              pattern: '{.,..}/**/*.d.ts',
              group: 'type',
              position: 'after',
            },
          ],
          pathGroupsExcludedImportTypes: ['type'],
          alphabetize: {
            order: 'asc',
            caseInsensitive: true,
          },
          'newlines-between': 'always',
        },
      ],
      // other rules
      // ...
    },
  },
)
```
