---
created: 2025-09-18T14:58:00.000+0800
modified: 2025-09-18T14:58:00.000+0800
---


# TanStack Query 使用笔记

> 官方文档 (v5): <https://tanstack.com/query/v5/docs/framework/vue/guides/network-mode>

TanStack Query 是一个强大的数据获取和状态管理库，支持 React、Vue、Angular 等多种前端框架。它简化了数据获取、缓存、同步和更新的过程，使开发者能够更专注于业务逻辑。

本文记录使用中的一些笔记和示例。

本文编写基于 v5 版本。

## 1 - 默认功能

### 数据引用的更新策略

默认情况下，仅当数据真正发生变化时，数据的引用才会更新 (通过 `structuralSharing` 实现)。这一默认配置有助于减少不必要的重新渲染。

### 自动重试

默认情况下，query 在失败时会自动重试 (默认重试 3 次，通过 `retry` 配置)，重试策略是指数退避 (exponential backoff)，默认 `retryDelay` 为 `3`。

### Stale

默认情况下，缓存数据被认为是 "stale" (过时的)，这意味着当组件重新挂载或窗口重新获得焦点时，数据会被重新获取。

如果配置了 `staleTime`，则在指定的时间内，数据会被认为是 "fresh" (新鲜的)，不会触发重新获取；超时后会变为 "stale"。

(Query 的 `refetchInterval` 配置与 `staleTime` 配置相互独立。)

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

### 2.1 Query 的状态

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

#### fetchStatus

> [fetchStatus](https://tanstack.com/query/v5/docs/framework/vue/guides/queries)

除了 `status` 外，Query 还有一个 `fetchStatus` 属性，表示数据获取的状态，它是以下三种之一:

- `isFetching` / `fetchStatus === 'fetching'`: queryFn 正在执行
- `isPaused` / `fetchStatus === 'paused'`: queryFn 想要执行，但被暂停了 (由于网络问题，暂停直到网络恢复。见 [Network Mode](https://tanstack.com/query/v5/docs/framework/vue/guides/network-mode))
- `fetchStatus === 'idle'`: queryFn 未执行，也未被暂停

#### 状态的例子

1. `status` 处于 `success` 状态时，通常 `fetchStatus` 也会是 `idle`，表示数据已经成功获取且没有正在进行的请求; `fetchStatus` 也可能是 `fetching`，但正在进行新的请求以更新数据。
2. query 被加载、且没有数据时，`status` 会是 `pending`，而 `fetchStatus` 会是 `fetching`; 如果没有网络连接，`fetchStatus` 也可能是 `paused`。

### 2.2 Query Key

Query Key 是一个唯一标识符，用于标识和缓存特定的 query。它通常是一个数组，包含查询的名称和相关参数。

`queryKey` 数组的元素可以是任何可以被 `JSON.stringify` 序列化的值。

`queryKey` 中的元素顺序很重要，改变顺序会被视为不同的 query。但是 `queryKey` 中的元素是 object 时，其属性的顺序不重要。

> [Query Keys are hashed deterministically!](https://tanstack.com/query/v5/docs/framework/vue/guides/query-keys#query-keys-are-hashed-deterministically)

如果 `queryFn` 依赖于某些参数，建议将这些参数包含在 `queryKey` 中:

- `queryKey` 数组可视为 `queryFn` 的依赖数组
- 每个请求会根据 `queryKey` 生成一个唯一的缓存键
- `queryKey` 中变量的变化会触发 `queryFn` 的重新执行，。

### 2.3 disabled

> [Disabling/Pausing Queries](https://tanstack.com/query/v5/docs/framework/vue/guides/disabling-queries)

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

##### isLoading 状态

Lazy Query 的初始状态是 `status === 'pending'` (pending 意味着还没有数据)。但由于还没有满足执行条件，所以也不适合用这个条件控制 UI 上的 "loading" 元素。

为此，可以用 `isLoading` flag 状态来控制 UI 上的 "loading" 元素。

它是一个派生的属性，等价于 `isPending && isFetching`。仅当 query 正在执行首次请求时，`isLoading` 为 true。

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
