# Vue3 UnoCSS 安装和配置

> 官方文档链接: [UnoCSS Vite Plugin](https://unocss.dev/integrations/vite)

写法查询

> <https://unocss.dev/interactive/>

## 1. 安装

```bash
pnpm add -D unocss
```

## 2. 初始化

### 配置 `vite.config.ts`

```typescript
import UnoCSS from 'unocss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    UnoCSS(),
  ],
})
```

### 创建 `uno.config.ts`

```js
// uno.config.ts
import { defineConfig } from 'unocss'

export default defineConfig({
  // ...UnoCSS options
})
```

### 在 `main.ts` 中引入 UnoCSS

```typescript
import 'virtual:uno.css'
```

## 3. 配置

### 3.1 Presets

使用预设的样式。

[Wind3 preset](https://unocss.dev/presets/wind3)

```bash
pnpm add -D @unocss/preset-wind3
```

配置 `uno.config.ts`:

```typescript
// uno.config.ts
import presetWind3 from '@unocss/preset-wind3'
import { defineConfig } from 'unocss'

export default defineConfig({
  presets: [
    presetWind3(),
  ],
})
```

#### (可选) rem-to-px

如果要搭配 PostCSS 的插件 `postcss-pxtorem` 使用，可以使用 [rem-to-px](https://unocss.dev/presets/rem-to-px) 预设。

> [PostCSS 配置 > 2.2 postcss-pxtorem & amfe-flexible](./Vue3%20PostCSS配置.md#22-postcss-pxtorem--amfe-flexible)

先把 rem 单位转换为 px 单位，再通过 PostCSS 插件 `postcss-pxtorem` 转换为 rem 单位。

```bash
pnpm add -D @unocss/preset-rem-to-px
```

配置 `uno.config.ts`:

```typescript
import presetRemToPx from '@unocss/preset-rem-to-px'

export default defineConfig({
  presets: [
    presetRemToPx(),
    // ...
  ],
})
```

### 3.2 自定义 CSS classes

`uno.config.ts` 中添加 rules，支持正则表达式。

```typescript
export default defineConfig({
  rules: [
    ['m-10', { margin: '10px' }],
    [/^p-(\d+)$/, (match) => ({ padding: `${match[1]}px` })],
  ],
})
```

### 3.3 CSS shortcuts

`uno.config.ts` 中添加 shortcuts，支持快捷 CSS:

```typescript
export default defineConfig({
  shortcuts: {
    btn: 'py-2 px-4 font-semibold rounded-lg shadow-md',
  },
})
```

同样支持正则表达式:

```typescript
export default defineConfig({
  shortcuts: [
    // you could still have object style
    {
      btn: 'py-2 px-4 font-semibold rounded-lg shadow-md',
    },
    // dynamic shortcuts
    [/^btn-(.*)$/, ([, c]) => `bg-${c}-400 text-${c}-100 py-2 px-4 rounded-lg`],
  ],
})
```

### 3.4 集成图标 (iconify)

安装所有图标 (~130MB)

```bash
pnpm i -D @iconify/json
```

安装指定图标库:

`pnpm add -D @iconify-json/[the-collection-you-want]`

例如:

```bash
# [Tabler](https://tabler-icons.io/)
pnpm add -D @iconify-json/tabler
# [Material Design Icons](https://materialdesignicons.com/)
pnpm add -D @iconify-json/material-symbols
# [Material Symbols](https://fonts.google.com/icons)
pnpm add -D @iconify-json/mdi
```

配置 `uno.config.ts`:

```typescript
import { presetIcons } from 'unocss'

export default defineConfig({
  presets: [
    presetIcons({
      prefix: 'i-',
      extraProperties: {
        display: 'inline-block',
        'vertical-align': 'middle'
      }
    })
  ],
})
```

在网站中查询图标：<https://icones.js.org/>，复制图标名称，在使用时添加 `i-` 前缀。

Examples:

```html
<!-- A basic anchor icon from Phosphor icons -->
<div class="i-ph-anchor-simple-thin" />
<!-- An orange alarm from Material Design Icons -->
<div class="i-mdi-alarm text-orange-400" />
<!-- A large Vue logo -->
<div class="i-logos-vue text-3xl" />
<!-- Sun in light mode, Moon in dark mode, from Carbon -->
<button class="i-carbon-sun dark:i-carbon-moon" />
<!-- Twemoji of laugh, turns to tear on hovering -->
<div class="i-twemoji-grinning-face-with-smiling-eyes hover:i-twemoji-face-with-tears-of-joy" />
```

可配合 VSCode 插件 `Iconify IntelliSense` 使用，提供图标实时预览和智能提示。

## 4. 扩展插件

### 4.1 Directives transformer

<https://unocss.dev/transformers/directives>

支持语法 `@apply`, `@screen` 和 `theme()`

```bash
pnpm add -D @unocss/transformer-directives
```

配置 `uno.config.ts`:

```typescript
import transformerDirectives from '@unocss/transformer-directives'

export default defineConfig({
  transformers: [transformerDirectives()],
})
```

#### `@apply` & `@screen` & `theme()` 语法

`@apply`: 应用 CSS 规则。

将原子化的样式名，合并成一个自定义的样式类名。

```css
.myLabel {
  @apply color-red font-bold;
}
```

```html
<div class="myLabel">Hello</div>
```

`@screen`: 响应式设计。

```css
@screen sm {
  .grid {
    --uno: grid-cols-3;
  }
}
```

`theme()`: 主题变量。

```css
.btn-blue {
  background-color: theme('colors.blue.500');
}
```

### 4.2 Variant Group transformer

<https://unocss.dev/transformers/variant-group>

```bash
pnpm add -D @unocss/transformer-variant-group
```

配置 `uno.config.ts`:

```typescript
import transformerVariantGroup from '@unocss/transformer-variant-group'

export default defineConfig({
  transformers: [transformerVariantGroup()],
})
```

#### 用法

```html
<div class="hover:(bg-blue-500 text-white) focus:(bg-blue-500 text-white)">
  Hover me
</div>
```

会被转换为:

```html
<div class="hover:bg-blue-500 hover:text-white focus:bg-blue-500 focus:text-white">
  Hover me
</div>
```

### 4.3 UnoCSS Reset

```bash
pnpm add @unocss/reset
```

> Usage: <https://unocss.dev/guide/style-reset#usage>

使用方法: 在 `main.ts` 中引入

```typescript
// https://unocss.dev/guide/style-reset#usage
// 以下任选其一
// Normalize.css
import '@unocss/reset/normalize.css'
// sanitize.css
import '@unocss/reset/sanitize/sanitize.css'
import '@unocss/reset/sanitize/assets.css'
// Eric Meyer
import '@unocss/reset/eric-meyer.css'
// Tailwind
import '@unocss/reset/tailwind.css'
```

## 5. ESLint 规则配置

> [UnoCSS ESLint Config](https://unocss.dev/integrations/eslint#eslint-config)

```bash
pnpm add -D @unocss/eslint-config
```

配置 `eslint.config.ts`:

> Vue3 + TypeScript 的 ESLint 规则使用 `defineConfigWithVueTs` 作为配置函数。
> 需要将 UnoCSS 的配置合并到其中。

```typescript
import unocss from '@unocss/eslint-config/flat'

export default defineConfigWithVueTs({
  // Other rules ...
  unocss,
})
```

## 6. VSCode 插件

安装 `UnoCSS` 插件，支持 UnoCSS 的语法高亮和智能提示。

可以在 `.vscode/extensions.json` 中添加推荐插件:

```json
{
  "recommendations": [
    "antfu.unocss"
  ]
}
```

## 7. Example

`unocss.config.ts`

```typescript
// unocss.config.ts
import transformerDirectives from '@unocss/transformer-directives'
import transformerVariantGroup from '@unocss/transformer-variant-group'
import presetWind3 from '@unocss/preset-wind3'
import presetRemToPx from '@unocss/preset-rem-to-px'
import { defineConfig, presetIcons } from 'unocss'

export default defineConfig({
  content: {
    pipeline: {
      exclude: ['node_modules', 'dist'],
    },
  },
  presets: [
    presetWind3({
      dark: 'class',
    }),
    presetIcons({
      collections: {
        tabler: () => import('@iconify-json/tabler').then((i) => i.icons),
        'material-symbols': () => import('@iconify-json/material-symbols').then((i) => i.icons),
      },
      extraProperties: {
        display: 'inline-block',
        'vertical-align': 'middle',
      },
    }),
    presetRemToPx(),
  ],
  transformers: [transformerDirectives(), transformerVariantGroup()],
  shortcuts: {
    'wh-full': 'w-full h-full',
    'flex-center': 'flex justify-center items-center',
    'flex-col-center': 'flex-center flex-col',
    'flex-x-center': 'flex justify-center',
    'flex-y-center': 'flex items-center',
    'i-flex-center': 'inline-flex justify-center items-center',
    'i-flex-x-center': 'inline-flex justify-center',
    'i-flex-y-center': 'inline-flex items-center',
    'flex-col': 'flex flex-col',
    'flex-col-stretch': 'flex-col items-stretch',
    'i-flex-col': 'inline-flex flex-col',
    'i-flex-col-stretch': 'i-flex-col items-stretch',
    'flex-1-hidden': 'flex-1 overflow-hidden',
    'absolute-lt': 'absolute left-0 top-0',
    'absolute-lb': 'absolute left-0 bottom-0',
    'absolute-rt': 'absolute right-0 top-0',
    'absolute-rb': 'absolute right-0 bottom-0',
    'absolute-tl': 'absolute-lt',
    'absolute-tr': 'absolute-rt',
    'absolute-bl': 'absolute-lb',
    'absolute-br': 'absolute-rb',
    'absolute-center': 'absolute-lt flex-center wh-full',
    'fixed-lt': 'fixed left-0 top-0',
    'fixed-lb': 'fixed left-0 bottom-0',
    'fixed-rt': 'fixed right-0 top-0',
    'fixed-rb': 'fixed right-0 bottom-0',
    'fixed-tl': 'fixed-lt',
    'fixed-tr': 'fixed-rt',
    'fixed-bl': 'fixed-lb',
    'fixed-br': 'fixed-rb',
    'fixed-center': 'fixed-lt flex-center wh-full',
    'nowrap-hidden': 'whitespace-nowrap overflow-hidden',
    'ellipsis-text': 'nowrap-hidden text-ellipsis',
    'transition-base': 'transition-all duration-300 ease-in-out',
  },
  theme: {
    colors: {
      primary: 'rgb(29,222,189)',
      nprogress: 'rgb(29,222,189)',
      dark: '#18181c',
    },
    fontSize: {
      'icon-xs': '0.875rem',
      'icon-small': '1rem',
      icon: '1.125rem',
      'icon-large': '1.5rem',
      'icon-xl': '2rem',
    },
  },
})
```
