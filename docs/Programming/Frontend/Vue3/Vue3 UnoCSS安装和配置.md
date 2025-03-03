# Vue3 UnoCSS 安装和配置

<https://unocss.dev/integrations/vite>

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

### 创建 `uno.config.js`

```js
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

### 3.2 自定义 CSS

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

### 3.4 集成图标

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

#### 1) 用法

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

#### 1) 用法

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

## 5. VSCode 插件

安装 `UnoCSS` 插件，支持 UnoCSS 的语法高亮和智能提示。

## 6. 写法查询

<https://unocss.dev/interactive/>
