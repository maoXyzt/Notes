# Vue3 配置使用图标和本地 SVG

需要安装如下依赖

* vite-plugin-svg-icons: 支持 SVG 图标
* unplugin-icons: 图标按需引入
* @vicons/ionicons4
* @iconify/vue
* @unocss/preset-icons

```bash
npm install @vicons/ionicons4 unplugin-icons vite-plugin-svg-icons
npm install -D @iconify/vue @unocss/preset-icons
```

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
