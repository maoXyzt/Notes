# Rust 工具链 & Cargo 国内源

本文使用阿里源作为 Rust 工具链和 Cargo 的国内源。

> <https://developer.aliyun.com/mirror/rustup>

## 1 - 用国内源安装 Rust 工具链

使用阿里云的安装脚本:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://mirrors.aliyun.com/repo/rust/rustup-init.sh | sh
```

## 2 - 配置 rustup 命令的国内源

配置如下环境变量:

```bash
export RUSTUP_UPDATE_ROOT=https://mirrors.aliyun.com/rustup/rustup
export RUSTUP_DIST_SERVER=https://mirrors.aliyun.com/rustup
```

## 3 - 配置 Cargo 的国内源

> <https://rust-guide.niqin.com/en-us/4-cargo/4.1-source-replacement.html>

目前阿里云镜像仅支持稀疏索引配置，需要您的 cargo 版本 >= 1.68。

Cargo 配置文件，配置文件位置如下：

* Windows:
  * `%USERPROFILE%\.cargo\config.toml`
* Linux & MacOS:
  * `$HOME/.cargo/config.toml`

Cargo 配置文件，内容如下：

```toml
[source.crates-io]
replace-with = 'aliyun'
[source.aliyun]
registry = "sparse+https://mirrors.aliyun.com/crates.io-index/"
```

---

PS:

其他可用源：

```toml
[source.crates-io]
registry = "https://github.com/rust-lang/crates.io-index"
replace-with = 'sjtu' # pick one of the following source
[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"

[source.sjtu]
registry = "sparse+https://mirrors.sjtug.sjtu.edu.cn/git/crates.io-index/"

[source.tuna]
registry = "sparse+https://mirrors.tuna.tsinghua.edu.cn/crates.io-index/"

[source.rustcc]
registry = "sparse+https://code.aliyun.com/rustcc/crates.io-index/"
```
