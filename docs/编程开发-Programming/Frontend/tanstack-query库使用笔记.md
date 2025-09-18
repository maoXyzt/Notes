---
created: 2025-09-18T14:58:00.000+0800
modified: 2025-09-18T14:58:00.000+0800
---


# TanStack Query 使用笔记

> 本文编写时基于 v5 版本的 Vue 框架版。
> 官方文档 (v5): <https://tanstack.com/query/v5/docs/framework/vue/guides/network-mode>

TanStack Query 是一个强大的数据获取和状态管理库，支持 React、Vue、Angular 等多种前端框架。它简化了数据获取、缓存、同步和更新的过程，使开发者能够更专注于业务逻辑。

本文不赘述最基础的用法，可以看官方的 [Quick Start](https://tanstack.com/query/v5/docs/framework/vue/quick-start)。

本文主要记录使用中的一些易混淆的概念、最佳实践。

## 1 - 默认功能

### 数据引用的更新策略

默认情况下，仅当数据真正发生变化时，数据的引用才会更新 (通过 `structuralSharing` 实现)。这一默认配置有助于减少不必要的重新渲染。

### 自动重试

默认情况下，query 在失败时会自动重试 (默认重试 3 次，通过 `retry` 配置)，重试策略是指数退避 (exponential backoff)，默认 `retryDelay` 为 `3`。

### Stale

默认情况下，缓存数据被认为是 "stale" (过时的)，这意味着当组件重新挂载或窗口重新获得焦点时，数据会被重新获取。

如果配置了 `staleTime`，则在指定的时间内，数据会被认为是 "fresh" (新鲜的)，不会触发重新获取；超时后会变为 "stale"。

(Query 的 `refetchInterval` 配置与 `staleTime` 配置相互独立。)

- `staleTime` 默认为 `0`，数据会立即变为 "stale"。
- `staleTime` 配置为 `Infinity` 时，数据永远不会变为 "stale"。

如果手动调用 `invalidateQueries`，数据也会变为 "stale"。

> [Query Invalidation](https://tanstack.com/query/v5/docs/framework/vue/guides/query-invalidation)

Stale 状态的 query 会在以下情况下自动重新获取:

- 新的 query 实例被挂载
- 窗口重新获得焦点
- 网络重新连接

### inactive Queries

当一个 query 没有活动的 `useQuery` / `useInfiniteQuery` 实例或 query observers 时，它会变为 "inactive" (非活动的)。

inactive queries 会在一段时间后被垃圾回收 (默认 5 分钟，通过 `gcTime` 配置)，以释放内存。

## 2 - Query

Query 通常用于异步获取和缓存数据。

### 2.1 Query Key

Query Key 是一个唯一标识符，用于标识和缓存特定的 query。它通常是一个数组，包含查询的名称和相关参数。

`queryKey` 数组的元素可以是任何可以被 `JSON.stringify` 序列化的值。

`queryKey` 中的元素顺序很重要，改变顺序会被视为不同的 query。但是 `queryKey` 中的元素是 object 时，其属性的顺序不重要。

> [Query Keys are hashed deterministically!](https://tanstack.com/query/v5/docs/framework/vue/guides/query-keys#query-keys-are-hashed-deterministically)

如果 `queryFn` 依赖于某些参数，建议将这些参数包含在 `queryKey` 中:

- `queryKey` 数组可视为 `queryFn` 的依赖数组
- 每个请求会根据 `queryKey` 生成一个唯一的缓存键
- `queryKey` 中变量的变化会触发 `queryFn` 的重新执行 (通过 stale 数据更新的机制)

### 2.2 Query 的状态

> [Query Basics](https://tanstack.com/query/v5/docs/framework/vue/guides/queries#query-basics)

Query 有两个状态: `status` 关注 `data` 的状态，而 `fetchStatus` 关注 queryFn 的执行状态。

#### status

Query 的状态(`status`)只能是以下三种之一:

- `isPending` / `status === 'pending'`: query 还没有数据
- `isError` / `status === 'error'`: query 请求失败
- `isSuccess` / `status === 'success'`: query 请求成功

除了上述三种状态外，Query 还有以下辅助属性:

- `error`: 当 `isError` 为 true 时，包含错误信息
- `data`: 当 `isSuccess` 为 true 时，包含请求到的数据

大部分情况下，只需要检查 `isPending` 和 `isError`，然后使用 `data` 即可。
(当检查过 `pending` 和 `error` 后，typescript 会自动推断出 `data` 的类型)

```vue
<template>
  <span v-if="isPending">Loading...</span>
  <span v-else-if="isError">Error: {{ error.message }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <ul v-else-if="data">
    <li v-for="todo in data" :key="todo.id">{{ todo.title }}</li>
  </ul>
</template>
```

#### fetchStatus

> [fetchStatus](https://tanstack.com/query/v5/docs/framework/vue/guides/queries)

除了 `status` 外，Query 还有一个 `fetchStatus` 属性，表示数据获取的状态，它是以下三种之一:

- `isFetching` / `fetchStatus === 'fetching'`: queryFn 正在执行
- `isPaused` / `fetchStatus === 'paused'`: queryFn 想要执行，但被暂停了 (由于网络问题，暂停直到网络恢复。见 [Network Mode](https://tanstack.com/query/v5/docs/framework/vue/guides/network-mode))
- `fetchStatus === 'idle'`: queryFn 未执行，也未被暂停

如果除了关注数据的状态外，还希望关注后台的数据获取状态时，可以用 `isFetching` 状态进行补充，如下组件示例:

```vue
<template>
  <div v-if="isFetching">Refreshing...</div> <!-- ⬅️ background fetching -->
  <span v-if="isPending">Loading...</span>
  <span v-else-if="isError">Error: {{ error.message }}</span>
  <!-- We can assume by this point that `isSuccess === true` -->
  <ul v-else-if="data">
    <li v-for="todo in data" :key="todo.id">{{ todo.title }}</li>
  </ul>
</template>
```

#### 状态的例子

1. `status` 处于 `success` 状态时，通常 `fetchStatus` 也会是 `idle`，表示数据已经成功获取且没有正在进行的请求; `fetchStatus` 也可能是 `fetching`，但正在进行新的请求以更新数据。
2. query 被加载、且没有数据时，`status` 会是 `pending`，而 `fetchStatus` 会是 `fetching`; 如果没有网络连接，`fetchStatus` 也可能是 `paused`。

### 2.3 禁用/暂停 Query

> [Disabling/Pausing Queries](https://tanstack.com/query/v5/docs/framework/vue/guides/disabling-queries)

#### `enabled` 选项

当 Query 的 `enabled` 为 false 时:

- 如果有缓存数据，则 query 的初始状态是 `status === 'success'`
- 如果没有缓存数据，则 query 的初始状态是 `status === 'pending'`，且 `fetchStatus === 'idle'`
- query 被挂载时不会自动触发 queryFn 的执行
- query 不会在后台自动重新获取
- `invalidateQueries` 和 `refetchQueries` 不会触发该 query 的重新获取
- `refetch` 方法会手动触发 queryFn 的执行，但如果使用了 `skipToken`，则不会触发 (见下文)

#### `skipToken`: 类型安全的替代方案

`skipToken` 是一个特殊的值，基本上可以认为它等同于 `enabled=false` (除了使用 `skipToken` 时，`refetch` 方法不会触发 queryFn 的执行)。

它可以在实现 disable 功能同时时，保持 query 的类型安全。

推荐 typescript 项目中使用 `skipToken` 代替 `enabled` 选项。

```typescript
import { useQuery, skipToken } from '@tanstack/vue-query'

const filter = ref('')
const queryFn = computed(() =>
  !!filter.value ? () => fetchTodos(filter) : skipToken,
)
const { data } = useQuery({
  queryKey: ['todos', filter],
  // ⬇️ disabled as long as the filter is undefined or empty
  queryFn: queryFn,
})
```

#### Lazy Queries

disable 功能可以用于实现 lazy queries。

一个常见的应用场景是，在搜索的场合，当用户输入搜索条件之前，不执行查询。

### 2.4 `isLoading` 状态

- 当没有网络连接时，Query 可能初始化为 `status === 'pending'`，但 `fetchStatus === 'paused'`
- Lazy Query 的初始状态可能是 `status === 'pending'` (意味着还没有数据)。但由于还没有满足执行条件，所以 `fetchStatus === 'idle'`

因此，`isPending` 不适合用来控制页面的 UI 上的 "loading" 元素。

Query 提供了 `isLoading`，它是一个派生的属性，等价于 `isPending && isFetching`。仅当 query 正在执行首次请求时，`isLoading` 为 true。

用 `isLoading` flag 就可以控制 "loading" 元素在初次获取数据时显示。

### 2.5 Query Invalidation

> [Query Invalidation](https://tanstack.com/query/v5/docs/framework/vue/guides/query-invalidation#query-matching-with-invalidatequeries)

#### 作用

调用 `invalidateQueries` 方法后，会发生以下事情:

- 使所有匹配的 query 变为 "stale"
- 如果 query 正在被使用 (通过 `useQuery` 或其他 hooks)，会自动在后台重新获取

#### Query 的匹配方式

当调用 `invalidateQueries` 方法时，可以传入一个 `queryKey` 参数，用于指定要 invalidation 的 query:

- 可以利用 `queryKey` 的 prefix 匹配机制实现匹配多个 query
  - (参考 [Query Filters](https://tanstack.com/query/v5/docs/framework/vue/guides/filters#query-filters))
- 可以传入 `exact: true` 参数，用于精确匹配 `queryKey`

```typescript
// Invalidate every query in the cache
queryClient.invalidateQueries()
// Invalidate every query with a key that starts with `todos`
queryClient.invalidateQueries({ queryKey: ['todos'] })
// Invalidate every query with a key that starts with `todos` and is exact
queryClient.invalidateQueries({ queryKey: ['todos'], exact: true })
```

更精确的匹配方式是，传入一个 `predicate` 函数，用于判断是否匹配:

```typescript
// Invalidate every query with a key that starts with `todos` and is exact
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'todos' && query.queryKey[1]?.version >= 10,
})
```

## 3 - Mutation

Mutations 通常用于创建、更新或删除数据的操作，或执行 server side-effects。

### 3.1 Mutation 的状态

> [Mutation](https://tanstack.com/query/v5/docs/framework/vue/guides/mutations)

Mutation 的状态(`status`)只能是以下三种之一:

- `isIdle` / `status === 'idle'`: mutation 当前处于空闲状态，或在 fresh/reset 状态
- `isPending` / `status === 'pending'`: mutationFn 正在执行
- `isError` / `status === 'error'`: mutationFn 执行失败
- `isSuccess` / `status === 'success'`: mutationFn 执行成功，且 data 可用

除了上述四种状态外，Mutation 还有以下辅助属性:

- `error`: 当 `isError` 为 true 时，包含错误信息
- `data`: 当 `isSuccess` 为 true 时，包含请求到的数据

### 3.2 Reset

通过 `reset` 方法可以清除 `error` 和 `data` 的值，并重置 `status` 为 `idle`。

### 3.3 Side Effects

可通过一系列选项，在 mutation 的 lifecycle 中的各个阶段执行特定的回调函数。

- `onMutate`: 在 mutationFn 执行前执行
- `onSuccess`: 在 mutationFn 执行成功后执行
- `onError`: 在 mutationFn 执行失败后执行
- `onSettled`: 在 mutationFn 执行完成后执行 (无论成功还是失败)

> [Mutation Side Effects](https://tanstack.com/query/v5/docs/framework/vue/guides/mutations#mutation-side-effects)

除了在用 `useMutation` 注册 mutation 实例时注册 side effects，也支持在调用 `mutate` 方法时传入上述相同的选项注册 side effects 回调函数。

用 `useMutation` 注册的回调函数会先执行，然后才是调用 `mutate` 时传入的回调函数。

### 3.4 mutateAsync

调用 mutateAsync 方法会返回一个 Promise，Promise 的 resolve 值是 mutationFn 的返回值，reject 值是 mutationFn 的错误信息。

### 3.5 重试

默认情况下，mutation 发生错误时不会自动重试。可通过 `retry` 选项配置重试行为。

如果是因为网络离线导致失败，则会在重连时按原来的顺序重试。

### 3.6 并发/顺序执行

默认情况下，mutation 会并发执行（除非是多次调用同一个 mutation）。

可配置 `scope` 选项，传入一个 `id` 值，使得 `scope.id` 相同的 mutation 顺序执行。

顺序执行的这些 mutation 会从 `isPaused` 为 true 的状态开始，逐一执行。

### 3.7 Mutation 执行后更新 Queries

> [Invalidations from Mutations](https://tanstack.com/query/v5/docs/framework/vue/guides/invalidations-from-mutations)
> [Automatic Query Invalidation After Mutations](https://tkdodo.eu/blog/automatic-query-invalidation-after-mutations)

Mutation 执行成功后，通常需要更新相关的 Queries。

可以通过在 `onSuccess` 回调函数中使用 queryClient 的 `invalidateQueries` 方法来更新相关的 Queries。

- 如果返回 Promise，则会在 Promise resolve 之前就更新 `data` 值，但在 Promise settle 之前 `isPending` 都不会变为 true。

## 4 - 高级用法

### 4.1 分页查询 (Paginated Queries)

> [Paginated/Lagged Queries](https://tanstack.com/query/v5/docs/framework/vue/guides/paginated-queries)

#### 基本实现方式

只需要在 `queryKey` 中加入分页信息的参数即可:

```typescript
const { data } = useQuery({
  queryKey: ['todos', page],
  queryFn: () => fetchTodos(page),
})
// 如果 pageSize 也是可变的，则需要将 pageSize 也加入 queryKey
```

不过这样会有一个问题: 每次请求新的分页数据时，query 会在 "success" 和 "pending" 状态之间来回转换跳跃。

通常这不是一个大问题。但如果想避免这种跳跃，可以考虑使用 `placeholderData` 选项。

#### 数据无缝更新

`placeholderData` 选项可以传入一个函数 (可以使用库内置的 `keepPreviousData` 函数)，用于返回 placeholder data。

效果如下:

- 在新的数据请求完成前，之前的 `data` 依然是可用的 (虽然 queryKey 已经发生了变化)
- 当新的数据请求完成时，`data` 会被新的数据无缝替换
- `isPlaceholderData` 为 true 时，表示 `data` 是 placeholder data (旧数据)

```typescript
import { useQuery, keepPreviousData } from '@tanstack/vue-query'

const { data } = useQuery({
  queryKey: ['todos', page],
  queryFn: () => fetchTodos(page),
  placeholderData: keepPreviousData,
})
```

### 4.2 无限滚动/无限加载请求 (Infinite Queries)

> [Infinite Queries](https://tanstack.com/query/v5/docs/framework/vue/guides/infinite-queries)

当实现无限滚动/无限加载功能时，我们需要不断得请求新的数据，将新数据添加到原有数据中。

利用 `useInfiniteQuery` 可以定义此类 query。

它与 `useQuery` 的区别在于:

- `data` 是一个包含了所有请求到的数据的对象
  - `data.pages` 是一个数组，包含了所有请求到的页面的数据
  - `data.pageParams` 是一个数组，包含了所有用于请求的页面参数
- 选项: `initialPageParam` 传入初始页面的查询参数
- 方法: `fetchNextPage` 用于请求下一页数据
- 选项: `getNextPageParam` 传入一个方法，用于确定是否存在下一页的可加载数据，返回相应的查询参数，用于加载它们
  - 函数签名: `getNextPageParam: (lastPage, allPages, lastPageParam): boolean | undefined | null`
- 派生属性: `hasNextPage` 当 `getNextPageParam` 返回值不为 `null` 或 `undefined` 时，值为 `true`
- 派生属性: `isFetchingNextPage` 用于区分是正在执行后台请求 (包括初始请求) 还是处于 "loading more" 状态

当使用双向滚动时，还可以使用:

- 方法: `fetchPreviousPage` 用于请求上一页数据
- 选项: `getPreviousPageParam` 传入一个方法，用于确定是否存在上一页的可加载数据，返回相应的查询参数，用于加载它们
  - 函数签名: `getPreviousPageParam: (firstPage, allPages, firstPageParam): boolean | undefined | null`
- 派生属性: `hasPreviousPage` 当 `getPreviousPageParam` 返回值不为 `null` 或 `undefined` 时，值为 `true`
- 派生属性: `isFetchingPreviousPage` 用于区分是正在执行后台请求 (包括初始请求) 还是处于 "loading more" 状态

#### 使用示例

一个基本的 "Load More" UI 的实现方式:

1. 等待 `useInfiniteQuery` 实例挂载后，自动请求第一组数据
2. 用 `getNextPageParam` 返回查询下一页时所需的查询参数
3. 调用 `fetchNextPage` 方法请求下一页数据

当数据状态变为 `stale` 后，重新请求时，会从第一组数据开始**顺序地**依次重新请求。

当 queryCache 中的数据被清空后，重新请求时，会只请求第一组数据。

infiniteQuery 的定义方法 (单向滚动):

```javascript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  getNextPageParam: (lastPage, pages) => ...,
})
```

当使用双向滚动时，infiniteQuery 的定义方法:

```javascript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  initialPageParam: 0,
  getNextPageParam: (lastPage, pages) => ...,
  getPreviousPageParam: (firstPage, pages) => ...,
})
```

#### 避免同时进行多个请求

需要注意: 一个 infiniteQuery 实例，一次只能有一个正在进行的请求。cache 是所有 pages 共享的，如果同时有多个请求，可能导致数据被覆盖。

为了避免数据冲突，建议在请求前检查 `isFetching` 状态:

```typescript
() => hasNextPage && !isFetching && fetchNextPage()
```

#### 逆向加载页面数据

有时候希望从最后一页数据开始逆向加载，可以结合 `select` 选项实现:

(实现方式: 同时反转 `data.pages` 和 `data.pageParams`)

```javascript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: fetchProjects,
  select: (data) => ({
    pages: [...data.pages].reverse(),
    pageParams: [...data.pageParams].reverse(),
  }),
})
```

#### 手动变更数据

用 `queryClient.setQueryData` 手动更新数据:

(实现方式: 同时更新 `data.pages` 和 `data.pageParams`)

```javascript
queryClient.setQueryData(['projects'], (data) => ({
  pages: data.pages.slice(1),
  pageParams: data.pageParams.slice(1),
}))
```

#### 限制一个 infiniteQuery 请求的页面数量

有时希望限制加载的页面数量，避免: 占用过多内存; 重新获取时，请求过多的页面。

为此，可以使用 "Limited Infinite Query" 模式。

该模式需要配置 `maxPages` 选项，限制存储的页面数量。同时需要配置 `getNextPageParam` 和 `getPreviousPageParam`，使得请求可以双向加载。
