---
type: note
aliases: []
created: 2026-05-22T00:56:31.000+0800
modified: 2026-05-22T00:56:40.001+0800
---

# cargo-release 的使用

> 参考: [crate-ci/cargo-release](https://github.com/crate-ci/cargo-release)

[`cargo-release`](https://github.com/crate-ci/cargo-release) 把发布一个 Rust crate 的几步动作 (改版本号 → commit → 打 tag → push → `cargo publish`) 合并成一条命令,适合需要频繁发布的项目。

手动发布流程见 [[发布Rust项目到crates.io]]。

## 1 - 安装

```bash
cargo install cargo-release
```

## 2 - 基本用法

```bash
# dry-run 预览将要做的事 (默认就是 dry-run!)
cargo release patch

# 真正执行
cargo release patch --execute
```

`<level>` 决定版本号怎么升:

| level | 效果 (例) |
| --- | --- |
| `patch` | `0.1.0` → `0.1.1` |
| `minor` | `0.1.0` → `0.2.0` |
| `major` | `0.1.0` → `1.0.0` |
| `0.3.0` | 直接指定为这个版本号 |

> **最常踩的坑**: 默认 dry-run,看着像执行成功但其实什么都没发生。要真正发布必须加 `--execute`。

一次完整的 `cargo release patch --execute` 会:

1. 把 `Cargo.toml` 的版本号从 `0.1.0` 改成 `0.1.1`
2. 提交这次改动 (commit message 默认是 `chore: release ...`)
3. 跑 `cargo publish` 发布到 crates.io
4. 打 git tag `v0.1.1`
5. 把 commit 和 tag push 到远端

## 3 - 常用 flag

| flag | 作用 |
| --- | --- |
| `--execute` | 真正执行(没有这个 flag 都是 dry-run) |
| `--no-publish` | 跳过 `cargo publish` (只 bump + commit + tag + push,publish 交给 CI) |
| `--no-push` | 不自动 push |
| `-p <crate>` | workspace 中只 release 指定的 crate |

## 4 - 最小配置: `release.toml`

放在项目根目录,覆盖一些默认行为:

```toml
# 只允许从 main 分支 release
allow-branch = ["main"]

# tag 名格式 (默认就是这个)
tag-name = "v{{version}}"
```

不需要配置也能用,默认值对单 crate 项目基本够用。

## 5 - 配合 CI 发布

如果 crates.io 的 token 只放在 CI 里,可以让 `cargo-release` 只负责 bump + tag + push,实际的 publish 交给 CI 监听 tag 触发:

```bash
cargo release patch --no-publish --execute
```

CI 配置见 [[发布Rust项目到crates.io]] 中的 GitHub Actions 章节。

## 6 - 相关阅读

* [[发布Rust项目到crates.io]]
* [[Rust项目结构]]
