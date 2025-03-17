# Vue3 自动按需引入组件（unplugin-vue-components）

## 安装依赖

* [unplugin-auto-import](https://github.com/unplugin/unplugin-auto-import)
* [unplugin-vue-components](https://github.com/unplugin/unplugin-vue-components)

```bash
pnpm i -D unplugin-auto-import
pnpm i -D unplugin-vue-components
```

## 配置

配置 `vite.config.ts`:

```typescript
// vite.config.ts
import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'

// ...
export default defineConfig({
  plugins: [
    // unplugin-auto-import
    AutoImport({
      // Filepath to generate corresponding .d.ts file.
      // Defaults to './auto-imports.d.ts' when `typescript` is installed locally.
      // Set `false` to disable.
      dts: 'src/typings/auto-imports.d.ts',
    }),
    // unplugin-vue-components
    Components({
      // generate `components.d.ts` global declarations,
      // also accepts a path for custom filename
      // default: `true` if package typescript is installed
      dts: 'src/typings/components.d.ts',
      resolvers: [
        NaiveUiResolver(),
      ],
    }),
  ]
})
```

其中，`dts` 为组件声明文件路径，需要手动创建，需要确保 `tsconfig.json` 中 `include` 配置包含该路径。

```json
{
  "include": [
    "src/**/*.d.ts",
  ]
}
```

resolvers 为组件解析器，可以自定义，也可以使用现成的解析器，如 `NaiveUiResolver`。

[Build-in resolvers](https://github.com/unplugin/unplugin-vue-components?tab=readme-ov-file#importing-from-ui-libraries)
