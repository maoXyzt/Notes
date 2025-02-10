# Vue3, Vite 配置 base 路径后，编译结果为空页面

## 1. 问题描述

在 Vue3 项目中使用 Vite 构建时，在 `vite.config.js` 中配置了 base 路径 (如 `/my-app/`)。

dev 模式下，页面正常显示;
编译后 (`npm run build` -> `npm run preview`) 打开为空白页面。

排查过程：

1. F12 打开控制台
2. 控制台无报错
3. 网络显示所有资源都加载成功，html/js/css 文件看起来正常

## 2. 问题原因

Vite 的 base 配置会影响到资源的引用路径。

通过 `import` 语句引入的资源，会被 Vite 处理成考虑 base 配置后的正确路径。

但是通过 `import()` 函数动态引入的资源，不会被 Vite 处理。这导致了路由配置中的懒加载组件无法正确加载。

如下写法就无法被正常处理：

```ts
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: import('../views/HomeView.vue'),   // ! buggy
    },
    {
      path: '/appliances',
      name: 'appliances',
      component: import('../views/AppliancesView.vue'), // ! buggy
    },
  ],
})
```

## 3. 解决方案

1. 将 `import()` 函数懒加载改为 `import` 语句
2. (推荐) 将 `import()` 函数调用改为 `() => import()` 函数调用
