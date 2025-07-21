# Vue3 PostCSS 配置

> Ref: <https://cn.vite.dev/guide/features#postcss>

## 1. 安装 PostCSS

```bash
pnpm i -D postcss-loader postcss
```

## 2. 插件

### 2.1 postcss-nesting / postcss-nested

* `postcss-nesting`: 支持 W3C 标准的 CSS 嵌套
* `postcss-nested`: 使用 sass 风格的嵌套

#### 2.1.1 安装

```bash
# 根据实际项目偏好，二选一:
pnpm add -D postcss-nesting
# or
pnpm add -D postcss-nested
```

#### 2.1.2 配置

配置 `vite.config.ts` 的 css 配置项:

```typescript
import postcssNesting from 'postcss-nesting'

export default defineConfig({
  css: {
    postcss: {
      plugins: [
        postcssNesting(),
        // ...
      ],
    },
  },
  // ...
})
```

### 2.2 `postcss-pxtorem`, `amfe-flexible`, `autoprefixer`

* `postcss-pxtorem`: 将 px 单位转换为 rem 单位
* `amfe-flexible`：根据设备宽度，修改根元素 html 的大小，以适配不一样终端。配置可伸缩布局方案，主要是将 1rem 设为 viewWidth/10。

通过这两个插件配合，实现适配移动端。

* `autoprefixer` 插件：自动添加浏览器前缀，免于手动添加

> 因为 css 中有一些属性还没有确定下来，标准规范还没有发布，许多浏览器支持的程度也不同，而且每个浏览器厂商同一个样式支持的写法也不同，所以要加前缀来达到各个浏览器兼容。将来统一了规范就不用写前缀了。

#### 2.2.1 安装

```bash
pnpm add postcss-pxtorem amfe-flexible autoprefixer
pnpm add -O @types/postcss-pxtorem
```

#### 2.2.2 配置 postcss-pxtorem

配置 `vite.config.ts` 的 css 配置项:

```typescript
import postcssPxtorem from 'postcss-pxtorem'

export default defineConfig({
  css: {
    postcss: {
      plugins: [
        postcssPxtorem({
          rootValue: 37.5, // 换算基数，默认值 16。 UI设计稿宽度 / 10
          unitPrecision: 3, // 允许REM单位增长到的十进制数字，小数点后保留的位数。
          propList: ['*'],
          // 可以用正则表达式排除某些文件夹的方法，例如 /(node_module)/
          // 如果想把前端UI框架内的px也转换成rem，请把此属性设为默认值 (false)
          exclude: /(node_module)/,
          // 要忽略并保留为px的选择器
          selectorBlackList: [],
          mediaQuery: false, // (布尔值) 允许在媒体查询中转换 px。
          minPixelValue: 1, // 设置要替换的最小像素值
        }),
        // ...
      ],
    },
  },
  // ...
})
```

`rootValue` 计算公式为: 设计稿宽度 / 10

假设设计稿为 375px，即 rootValue 设为 37.5，意味着每个 rem 单位对应设计稿中的 37.5px

#### 2.2.3 引入 `amfe-flexible`

在 `src/main.ts` 中引入 `amfe-flexible` 文件：

```typescript
import 'amfe-flexible'
```

#### 2.2.4 Autoprefixer

```typescript
import autoprefixer from 'autoprefixer'

export default defineConfig({
  css: {
    postcss: {
      plugins: [
        // ...
        autoprefixer,
        // ...
      ],
    },
  },
  // ...
})
```
