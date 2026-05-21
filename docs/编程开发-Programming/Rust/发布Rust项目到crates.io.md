---
type: note
aliases: []
created: 2026-05-22T00:24:20.000+0800
modified: 2026-05-22T00:35:10.955+0800
---

> 参考:
>
> * [Publishing on crates.io - The Cargo Book](https://doc.rust-lang.org/cargo/reference/publishing.html)
> * [发布到 crates.io - Rust 语言圣经](https://course.rs/cargo/reference/publishing-on-crates.io.html)

[crates.io](https://crates.io) 是 Rust 官方的包注册中心 (registry)，是 Rust 生态中绝大多数三方库的分发渠道。

本文记录将一个 Rust 项目 (lib crate) 发布到 crates.io 的完整流程。

## 1 - 注册账号并获取 API Token

发布 crate 前需要一个 crates.io 账号:

1. 访问 <https://crates.io>，使用 GitHub 账号登录 (目前 crates.io 仅支持 GitHub OAuth 登录)。
2. 首次登录后需要在 [Account Settings](https://crates.io/settings/profile) 中确认邮箱地址 —— **未验证邮箱无法发布 crate**。
3. 进入 [API Tokens](https://crates.io/settings/tokens) 页面，点击 `New Token` 创建一个新的 token。
	 * 可以为 token 配置 scope (例如限定只能 publish 某个 crate)、过期时间。
	 * Token 只会显示一次，请妥善保存。

## 2 - 登录 cargo

在本地用 cargo 登录 crates.io:

```bash
cargo login
```

执行后会提示输入 token，粘贴后回车即可。Token 会被保存到 `$CARGO_HOME/credentials.toml` (默认是 `~/.cargo/credentials.toml`)。

也可以一行命令完成:

```bash
cargo login <your-token>
```

> 注意: 这种方式会把 token 写到 shell 历史中，不推荐。

## 3 - 完善 `Cargo.toml` 中的元数据

发布到 crates.io 的 crate 必须在 `Cargo.toml` 的 `[package]` 中提供足够的元数据，否则 `cargo publish` 会报错。

最小可发布的 `[package]` 示例:

```toml
[package]
name = "my_awesome_crate"
version = "0.1.0"
edition = "2021"
description = "A short description of my crate"
license = "MIT OR Apache-2.0"
repository = "https://github.com/your-name/my_awesome_crate"
readme = "README.md"
```

常用的元数据字段:

| 字段 | 说明 | 是否必填 |
| --- | --- | --- |
| `name` | crate 名称，需在 crates.io 上 **全局唯一** | 必填 |
| `version` | 语义化版本号 (SemVer) | 必填 |
| `edition` | Rust edition (如 `2021`, `2024`) | 必填 |
| `description` | 一句话描述，会显示在 crates.io 搜索结果中 | 必填 |
| `license` 或 `license-file` | 许可证 SPDX 标识符，或本地许可证文件路径 | 必填 (二选一) |
| `repository` | 源码仓库 URL | 推荐 |
| `homepage` | 项目主页 URL | 推荐 |
| `documentation` | 文档地址 (不填则默认指向 docs.rs) | 可选 |
| `readme` | README 文件路径，会显示在 crates.io 项目页 | 推荐 |
| `keywords` | 关键词数组，最多 5 个，每个最多 20 字符 | 推荐 |
| `categories` | 分类数组，需使用 crates.io 预定义的 [分类列表](https://crates.io/category_slugs) | 推荐 |

> `license` 字段使用 [SPDX](https://spdx.org/licenses/) 标识符。Rust 项目常用 `MIT OR Apache-2.0` 双协议，与 Rust 标准库一致。

## 4 - 预检查: `cargo publish --dry-run`

正式发布前，强烈建议先执行一次 dry-run，模拟整个 publish 过程但不实际上传:

```bash
cargo publish --dry-run
```

dry-run 会:

* 检查 `Cargo.toml` 元数据是否完整
* 编译 crate，确认能在 crates.io 环境 (无本地未提交修改、无 path 依赖) 下成功构建
* 打包要上传的文件，可用 `cargo package --list` 查看具体打包内容

```bash
cargo package --list
```

### 4.1 控制打包内容

默认情况下 cargo 会打包 `src/` 目录、`Cargo.toml`、`README`、`LICENSE` 等文件，并 **忽略 `.gitignore` 中列出的文件**。

如需更精细地控制打包内容，可在 `[package]` 中使用 `include` 或 `exclude`:

```toml
[package]
# 二选一，不要同时使用
exclude = ["assets/raw/**", "tests/fixtures/**"]
# include = ["src/**", "Cargo.toml", "README.md", "LICENSE*"]
```

> 注意: 打包后的 `.crate` 文件大小上限为 **10 MiB**，超过会被 crates.io 拒绝。

## 5 - 正式发布: `cargo publish`

确认 dry-run 通过后，执行:

```bash
cargo publish
```

发布成功后，crate 会立即出现在 `https://crates.io/crates/<name>`，并由 [docs.rs](https://docs.rs) 自动构建文档 (通常几分钟内可访问)。

> **重要**: 一旦发布成功，**版本号无法被覆盖，也无法被删除**(只能 yank, 见下文)。所以建议先 dry-run，确认无误后再正式发布。

## 6 - 版本管理

### 6.1 发布新版本

更新代码后，修改 `Cargo.toml` 中的 `version` 字段，遵循 [SemVer](https://semver.org/lang/zh-CN/) 规则:

* `0.1.0` → `0.1.1`: 向后兼容的修复
* `0.1.0` → `0.2.0`: 0.x 阶段视为破坏性变更
* `1.0.0` → `1.1.0`: 向后兼容的新功能
* `1.0.0` → `2.0.0`: 破坏性变更

然后再次执行 `cargo publish` 即可。

### 6.2 撤回版本: `cargo yank`

如果发现某个已发布版本有严重问题 (如安全漏洞)，可以 **yank(撤回)** 该版本:

```bash
# 撤回指定版本
cargo yank --version 0.1.1

# 取消撤回
cargo yank --version 0.1.1 --undo
```

Yank 的语义:

* **已经在 `Cargo.lock` 中锁定此版本的项目** 仍然可以继续下载和使用
* **新项目** 在解析依赖时不再考虑这个版本
* Yank **不会删除版本内容**，crates.io 不允许真正删除已发布的版本

## 7 - 用 GitHub Actions 自动发布

手动 `cargo publish` 适合个人项目，但当项目有协作者、或需要稳定的发布节奏时，把发布流程放到 CI 里能避免 " 在我本地能 publish" 之类的问题 (本地环境差异、忘记打 tag、token 泄露等)。

### 7.1 配置 CARGO_REGISTRY_TOKEN

在 crates.io [API Tokens](https://crates.io/settings/tokens) 页面创建一个 **专用于 CI** 的 token，scope 建议限定为只能 `publish-update`(及首次发布所需的 `publish-new`) 对应的 crate。

然后在 GitHub 仓库的 `Settings → Secrets and variables → Actions` 中新建 secret，命名为 `CARGO_REGISTRY_TOKEN`，将 token 粘贴进去。

> cargo 会自动识别名为 `CARGO_REGISTRY_TOKEN` 的环境变量，无需在 workflow 中额外执行 `cargo login`。

### 7.2 方案 A: 推送 git tag 触发发布

最常见的做法是: 在本地把版本号在 `Cargo.toml` 中改好、合并到 main 后，打一个 `v<version>` 形式的 tag 并推送，CI 自动发布对应版本。

`.github/workflows/publish.yml`:

```yaml
name: Publish to crates.io

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - name: Verify tag matches Cargo.toml version
        run: |
          TAG_VERSION="${GITHUB_REF_NAME#v}"
          CARGO_VERSION=$(cargo metadata --no-deps --format-version 1 \
            | jq -r '.packages[0].version')
          if [ "$TAG_VERSION" != "$CARGO_VERSION" ]; then
            echo "Tag $TAG_VERSION != Cargo.toml version $CARGO_VERSION"
            exit 1
          fi

      - name: Publish
        env:
          CARGO_REGISTRY_TOKEN: ${{ secrets.CARGO_REGISTRY_TOKEN }}
        run: cargo publish
```

关键点:

* `on.push.tags: ["v*"]` 只在推送形如 `v0.1.0` 的 tag 时触发，避免误发布。
* "tag 与 `Cargo.toml` 版本一致性 " 校验可防止 tag 名和实际版本号对不上。
* 推送 tag: `git tag v0.1.0 && git push origin v0.1.0`。

### 7.3 方案 B: 手动触发 (workflow_dispatch)

如果不想为发布维护 tag，可以改为手动触发:

```yaml
on:
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - name: Publish
        env:
          CARGO_REGISTRY_TOKEN: ${{ secrets.CARGO_REGISTRY_TOKEN }}
        run: cargo publish
```

在 GitHub 仓库的 `Actions` 标签页选择该 workflow，点击 `Run workflow` 即可触发。

### 7.4 发布前先跑测试

`cargo publish` 本身会编译 crate，但不会跑测试。建议把 publish job 依赖于一个 test job，测试不通过就不发布:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test --all-features

  publish:
    needs: test
    runs-on: ubuntu-latest
    # ...
```

### 7.5 Workspace 多 crate 发布

如果项目是 workspace 且需要发布多个 crate，注意:

* 存在依赖关系的 crate 必须按依赖顺序依次 publish (被依赖的先发)。
* crates.io 的 registry index 有 **传播延迟**(通常几秒到几十秒)，紧接着发布依赖它的 crate 可能会因为找不到刚发布的版本而失败 —— 在两个 `cargo publish` 之间加一个短暂的等待，或使用 [`cargo-release`](https://github.com/crate-ci/cargo-release)、[`release-plz`](https://github.com/MarcoIeni/release-plz) 这类工具自动处理顺序与等待。

> `release-plz` 还能根据 conventional commits 自动 PR 出版本号变更和 changelog，适合需要稳定发布节奏的项目。

## 8 - 常见问题

### 8.1 crate 名称冲突 / 抢注

crates.io 上的 crate 名称是 **先到先得，全局唯一**。如果想用的名称已被占用，只能换名。

> 出于反抢注政策，crates.io 团队会处理明显的恶意抢注，但日常发布中尽量提前确认名称可用。

### 8.2 依赖 git 或 path 的 crate 无法发布

`cargo publish` 要求所有依赖都来自 registry。如果 `Cargo.toml` 中有 `git = "..."` 或 `path = "..."` 形式的依赖，需要先把这些依赖也发布到 crates.io，或者改为 registry 依赖。

workspace 内的本地依赖可以同时使用 `path` 和 `version`，cargo 在 publish 时会自动使用 `version`:

```toml
[dependencies]
my_internal_lib = { path = "../my_internal_lib", version = "0.1.0" }
```

### 8.3 工作目录有未提交修改

默认情况下，`cargo publish` 会检查 git 工作目录是否干净，有未提交修改时会报错。可用 `--allow-dirty` 跳过此检查 (不推荐)。

### 8.4 README 中的相对路径图片无法显示

crates.io 项目页渲染 README 时，相对路径的图片/链接可能无法解析。建议在 README 中使用绝对 URL(指向 GitHub raw 内容或图床)。

## 9 - 相关阅读

* [[Rust项目结构]]
* [[Rust工具链&Cargo国内源]]
