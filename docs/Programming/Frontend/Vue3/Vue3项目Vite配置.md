# Vue3 项目 Vite 配置

配置 `vite.config.ts` 文件。

<https://vitejs.dev/config/>

## 1. Example

```typescript
import * as child from 'child_process'

const commitHash = () => {
  try {
    return child.execSync('git rev-parse --short HEAD').toString().trim()
  } catch (e) {
    return undefined
  }
}

export default defineConfig({
  css: {
    postcss: {},
  },
  define: {
    'process.env': {
      COMMIT_HASH: commitHash(),
    },
  },
  base: '/',
  server: {
    host: '0.0.0.0',
    port: 5055,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      },
      '/statics': {
        target: 'http://10.151.5.225:32808',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/statics/, ''),
      },
    },
    warmup: {
      clientFiles: ['./src/components/**/*.vue', './src/plugins/*.ts'],
    },
  },
  build: {
    rollupOptions: {
      // Customize the Rollup config here
      output: {
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            // 让每个插件都打包成独立的文件
            if (id.includes('node_modules/.pnpm')) {
              return id.toString().split('node_modules/.pnpm/')[1].split('/')[0].toString()
            } else {
              return id.toString().split('node_modules/')[1].split('/')[0].toString()
            }
          }
        },
        chunkFileNames: 'js/[name]-[hash].js', // 引入文件名的名称
        entryFileNames: 'js/[name]-[hash].js', // 包的入口文件名称
        assetFileNames: '[ext]/[name]-[hash].[ext]', // 资源文件像 字体，图片等
      },
    },
  },
  esbuild: {
    // Drop debugger in production.
    drop: process.env.NODE_ENV === 'production' ? ['debugger'] : [],
  },
})
```

## 2. 配置项说明

<!-- TODO -->

### 2.1 css

### 2.2 define

### 2.3 base

### 2.4 server

### 2.5 build

### 2.6 esbuild
