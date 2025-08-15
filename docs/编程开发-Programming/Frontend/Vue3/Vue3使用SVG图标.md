# Vue3 配置使用图标和本地 SVG

需要安装如下依赖

* `vite-plugin-svg-icons`: 支持 SVG 图标
* `unplugin-icons`: 图标按需引入
* `@vicons/ionicons5`: 封装了 [Ionicons v5](https://ionic.io/ionicons/) 图标的 Vue 组件库
  * 属于 [xicons](https://www.xicons.org/#/) 项目的一部分: <https://github.com/07akioni/xicons?tab=readme-ov-file#icon-packages>
* `@iconify/vue`
* `@unocss/preset-icons`

```bash
npm install unplugin-icons vite-plugin-svg-icons
npm install -D @vicons/ionicons5 @iconify/vue @unocss/preset-icons
```

## 配置

`vite.config.ts`: 配置如下插件

```typescript
// vite.config.ts
import path from 'node:path'
import { FileSystemIconLoader } from 'unplugin-icons/loaders'
import IconsResolver from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'

const viteIconPrefix = 'icon'
const viteIconLocalPrefix = 'icon-local'
/** 本地 svg 图标集合名称 */
const collectionName = viteIconLocalPrefix.replace(`${viteIconPrefix}-`, '')
const localIconPath = path.join(process.cwd(), 'src/assets/icons')  // 本地 svg 图标路径

export default defineConfig({
  plugins: [
    // ...
    // unplugin-vue-components
    Components({
      // ...
      resolvers: [
        // ...
        IconsResolver({
          customCollections: [collectionName],
          componentPrefix: viteIconPrefix,
        }),
      ],
    }),
    // vite-plugin-svg-icons
    createSvgIconsPlugin({
      iconDirs: [localIconPath],
      symbolId: `${viteIconLocalPrefix}-[dir]-[name]`,
      inject: 'body-last',
      customDomId: '__SVG_ICON_LOCAL__',
    }),
    // [unplugin-icons](https://github.com/antfu/unplugin-icons)
    Icons({
      compiler: 'vue3',
      customCollections: {
        [collectionName]: FileSystemIconLoader(localIconPath, (svg) =>
          svg.replace(/^<svg\s/, '<svg width="1em" height="1em" '),
        ),
      },
      scale: 1,
      defaultClass: 'inline-block',
    }),
    // ...
  ],
  // ...
})
```

## 使用

* svg 图标

```html
<IconLocalFitScreen class="text-40px c-#adbad3 hover-c-#fff"></IconLocalFitScreen>
```

* `@vicons/ionicons5`

```html
<Icon-material-symbols:play-circle-outline-rounded
  class="text-40px c-#adbad3 hover-c-#fff"
/>
<Icon-material-symbols:pause-circle-outline-rounded
  class="text-40px c-#adbad3 hover-c-#fff"
/>
```

* `iconify/vue`

```html
<Icon icon="mdi-light:home" />
```

* `@unocss/preset-icons`

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
