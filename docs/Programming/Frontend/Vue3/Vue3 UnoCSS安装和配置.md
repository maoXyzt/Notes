# Vue3 UnoCSS 安装和配置

<https://unocss.dev/integrations/vite>

## 安装

```bash
pnpm add -D unocss
```

## 初始化配置

配置 `vite.config.ts`:

```typescript
import UnoCSS from 'unocss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    UnoCSS(),
  ],
})
```

创建 `uno.config.js`:

```js
import { defineConfig } from 'unocss'
import presetIcons from '@unocss/preset-icons'
import presetUno from '@unocss/preset-uno'
import transformerDirectives from '@unocss/transformer-directives'
import transformerVariantGroup from '@unocss/transformer-variant-group'


export default defineConfig({
  // ...UnoCSS options
})
```

在 `main.ts` 中引入 UnoCSS:

```typescript
import 'virtual:uno.css'
```

## VSCode 插件

安装 UnoCSS 插件，支持 UnoCSS 的语法高亮和智能提示。

## 写法查询

<https://unocss.dev/interactive/>

## 自定义 CSS

`uno.config.ts` 中添加 rules，支持正则表达式。

```typescript
export default defineConfig({
  rules: [
    ['m-10', { margin: '10px' }],
    [/^p-(\d+)$/, (match) => ({ padding: `${match[1]}px` })],
  ],
})
```

## 快捷 CSS

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

## 集成图标

```bash
pnpm i -D @iconify/json
```

配置 `uno.config.ts`:

```typescript
import { presetWind, presetIcons } from 'unocss'

export default defineConfig({
  presets: [
    presetWind(),
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

在该网站中查询图标：<https://icones.js.org/，复制图标名称，在使用时添加> `i-` 前缀。

```html
<div class="i-material-symbols:calendar-today"></div>
```

## 扩展插件

### transformer

支持语法 @apply, @screen 和 theme()


