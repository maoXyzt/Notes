# Rust 项目结构

Rust 中，代码的组织管理层级分为：

* **Packages**(项目、工程、软件包)：一个 Cargo 提供的 feature，可以用来构建、测试和分享包
  * 包含独立的 `Cargo.toml` 文件，以及因为功能性被组织在一起的一个或多个 Crate
* **Crate**(包)：一个由多个 Module 组成的树形结构，可以作为三方库进行分发，也可以生成可执行文件进行运行
* **Module**(模块)：一个文件可以包含多个 Module, 也可以一个文件一个 Module。可以认为 Module 是真实项目中的代码组织单元

这些概念与其他语言中的概念类似，但 **名称不同，翻译时也会造成一定的困惑**，需要注意区分。

另外还有一个概念：**WorkSpace**(工作空间)：对于大型项目，可以进一步将多个 Packages 联合在一起，组织成 WorkSpace。

## 1 - 基本项目结构: bin 项目 vs lib 项目

Rust 项目（Package）分为 bin 和 lib 两种类型。bin 项目是可执行的，lib 项目是库文件。

* bin 项目: 用于创建可执行文件（即二进制文件）。它通常包含一个 main 函数作为程序的入口点。每个 bin 项目都会生成一个独立的可执行文件。
* lib 项目: 用于创建库文件，可以被其他 Rust 项目作为依赖引用。根据配置，可以生成生成一个 `.rlib` (Rust 库)，动态链接库（如 `.so`、`.dylib` 或 `.dll` 文件）或静态库（如 `.a` 或 `.lib` 文件）

一个 Rust 项目（Package）可以同时拥有一个 lib 目标和多个 bin 目标。这意味着你可以在同一个项目中既定义一个库，又定义多个可执行程序，这些可执行程序可以使用该库的功能。

Rust 项目的基本结构如下：

### 1.1 bin 项目

使用 `cargo new` 命令创建一个 bin 项目(package)，命令如下：

```bash
cargo new my_bin
# `--bin` 是默认选项，等价于:
cargo new --bin my_bin
```

项目的结构如下：

```bash
my_project
├── Cargo.toml
└── src
    └── main.rs
```

```rust
// src/main.rs
fn main() {
    println!("Hello, world!");
}
```

`main.rs` 是 bin Crate 的根模块，`src/main.rs` 这个 Crate 与 Package 的名称相同，。

可以用 `cargo run` 运行项目。

用 `cargo build` 编译后会生成一个可执行文件。

### 1.2 lib 项目

使用 `cargo new --lib` 命令创建一个库(lib)项目，命令如下：

```bash
cargo new --lib my_lib
```

```bash
my_project
├── Cargo.toml
└── src
    └── lib.rs
```

`src/lib.rs` 是库的根模块，编译后会生成一个库文件。

Cargo 惯例:

> 如果一个 Package 包含有 `src/lib.rs`，是意味它包含有一个库类型的同名包 my-lib，该包的根文件是 src/lib.rs。

```rust
// src/lib.rs
pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
```

lib 项目不能运行 `cargo run` 命令，因为它没有 `main` 函数。

## 2 - Package(项目), Crate(包) 和 Module(模块)

### 2.1 Package(项目) vs Crate(包)

* Package 是一个项目工程，而 Crate 只是一个编译单元。
  * 一个 Package 中最多只能有 **一个** lib crate，但可以有 **多个** bin crate。
* Crate 是一个独立的可编译单元，它编译后会生成一个可执行文件或者一个库。

同一个 Crate 中不能有同名的 Rust 类型，但是在不同 Crate 中就可以。

#### (1) Crate root 与名称约定

Cargo 约定:

* 唯一的 lib crate: 入口文件(crate root)是 `src/lib.rs`, lib 名称与 Package 名称相同。
* 默认的 bin crate: 入口文件(crate root)是 `src/main.rs`，bin 名称与 Package 名称相同，入口函数为 `fn main()`。
* 额外的 bin crate: 入口文件(crate root)是 `src/bin/` 目录下的文件，bin 名称与文件名相同，入口函数为 `fn main()`。

#### (2) Crate 命名规范

推荐 Crate 命名遵循 snake_case 风格 (官方建议尽可能使用单个单词的名称)。

* 其实只有 bin crate 的名称是可以通过文件名自定义的

个人建议 Package 也遵循 snake_case 风格 (因为 Package name 也是默认 lib/bin crate 的名称)。

> [Naming conventions](https://doc.rust-lang.org/1.0.0/style/style/naming/README.html)

### 2.2 Module(模块)

> [模块 Module](https://course.rs/basic/crate-module/module.html)

Module 可以将 Crate 中的代码按照功能性进行重组，最终实现更好的可读性及易用性。同时，我们还能非常灵活地去控制代码的可见性，进一步强化 Rust 的安全性。

#### (1) Module 的定义

用 `mod` 关键字定义一个 Module:

* Module 可以嵌套
* Module 中可以定义各种 Rust 类型，包括结构体、枚举、函数、常量等
* 一个 Module 的代码必须定义在一个文件中

Example:

```rust
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}
        fn seat_at_table() {}
    }
    mod serving {
        fn take_order() {}
        fn serve_order() {}
        fn take_payment() {}
    }
}
```

#### (2) Module 的命名规范

推荐 Module 命名遵循 snake_case 风格。

#### (3) Module 内容的引用路径

想要使用一个 Rust 类型，就需要知道它的路径，在 Rust 中，这种路径有两种形式：

* 绝对路径，从 Package root 开始，路径名以 crate 名或者 `crate::` 作为开头
* 相对路径，从当前 Module 开始，以 `self::`，`super::` 或当前 Module 的标识符作为开头

#### (4) 可见性

默认情况下，Rust 中的 Module 是私有的：

* 私有 Module 中的内容不能被外部访问(包括父 Module)，但可以被子 Module 访问

用 `pub` 关键字将 Module 声明为公有的，

* 公有 Module 中允许外部访问 Module 内 **声明为公有的内容**
* enum(枚举) 成员的默认可见性与 enum 自身相同
* struct(结构体) 成员的默认可见性为私有的

#### (5) 定义与实现分离

Module 的定义与实现可以分离。

用 `mod` 关键字定义 Module，不编写实现代码:

```rust
// src/lib.rs
mod front_of_house;
```

Module 的代码实现可以写在如下文件中:

* (推荐, rustc >= 1.30) 与声明文件同目录下的、与 Module 同名的文件中: `src/front_of_house.rs`
* (不推荐) 与声明文件同目录下的、与 Module 同名的目录中的 `mod.rs` 文件中: `src/front_of_house/mod.rs`

同理，当一个 Module 有许多子模块时，我们也可以通过文件夹的方式来组织这些子模块。

```bash
src
├── front_of_house
│   ├── hosting.rs
│   └── serving.rs
├── front_of_house.rs
└── lib.rs
```

```rust
// src/front_of_house.rs
pub mod hosting;
pub mod serving;
```

```rust
// src/front_of_house/hosting.rs
pub fn add_to_waitlist() {}
pub fn seat_at_table() {}
```

```rust
// src/front_of_house/serving.rs
pub fn take_order() {}
pub fn serve_order() {}
pub fn take_payment() {}
```

注意: 用 `pub` 显示控制需要暴露的 Module 内容。

## 3 - 标准的 Package 目录结构

> 参考:
>
> * [Package 目录结构 - Rust 语言圣经(Rust Course)](https://course.rs/cargo/guide/package-layout.html)

```bash
.
├── Cargo.lock
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── main.rs
│   └── bin/
│       ├── named-executable.rs
│       ├── another-executable.rs
│       └── multi-file-executable/
│           ├── main.rs
│           └── some_module.rs
├── benches/
│   ├── large-input.rs
│   └── multi-file-bench/
│       ├── main.rs
│       └── bench_module.rs
├── examples/
│   ├── simple.rs
│   └── multi-file-example/
│       ├── main.rs
│       └── ex_module.rs
└── tests/
    ├── some-integration-tests.rs
    └── multi-file-test/
        ├── main.rs
        └── test_module.rs
```

这也是 Cargo 推荐的目录结构，解释如下：

* `Cargo.toml` 和 `Cargo.lock` 保存在 package 根目录下
* `src` 目录: 源代码
* `src/lib.rs`: 默认的 lib 包根
* `src/main.rs`: 默认的二进制包根
* `src/bin/`: 其它二进制包根
* `benches/`: 基准测试 benchmark
* `examples/`: 示例代码
* `tests/`: 集成测试代码

bin、tests、examples 等目录路径都可以通过配置文件进行配置，它们被统一称之为 [Cargo Target](https://course.rs/cargo/reference/cargo-target.html)。

> * Library: 库对象
> * Binary: 二进制对象
> * Examples: 示例对象
> * Tests: 测试对象
> * Benches: 基准性能对象

## 4 - WorkSpace(工作空间): 大型项目

> [工作空间 Workspace](https://course.rs/cargo/reference/workspaces.html)

一个 WorkSpace(工作空间)是由多个 package 组成的，它们共享同一个 `Cargo.lock` 文件、输出目录和一些设置(例如 profiles : 编译器设置和优化)。

组成 WorkSpace 的 packages 被称之为工作空间的 member(成员)。

定义了 `[workspace]` 的 `Cargo.toml` 文件所在的目录就是这个 Workspace 的根(root)目录。

根据是否定义了 `[package]`，工作空间有两种类型:

* root package
* virtual manifest (虚拟清单)

### 4.1 root package

若一个 package 的 `Cargo.toml` 包含了 `[package]` 的同时又包含了 `[workspace]` 部分，则该 package 被称为 Workspace 的 root package。

例如:

* [ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/Cargo.toml) 项目

### 4.2 virtual manifest

如果一个 `Cargo.toml` 文件只包含 `[workspace]` 部分，没有包含 `[package]`，则它被称为 virtual manifest(虚拟清单)。

对于没有主 package 的场景或你希望将所有的 package 组织在单独的目录中时，这种方式就非常适合。

例如:

* [rust-analyzer](https://github.com/rust-analyzer/rust-analyzer) 项目

### 4.3 Workspace 的关键特征

Workspace 的几个关键点在于:

* 所有的 package 共享同一个 `Cargo.lock` 文件，该文件位于 workspace 的根目录中
* 所有的 package 共享同一个输出目录，该目录默认的名称是 `target` ，位于 workspace 的根目录下
* 只有 workspace 根目录的 `Cargo.toml` 才能包含 `[patch]`, `[replace]` 和 `[profile.*]`，而成员的 `Cargo.toml` 中的相应部分将被自动忽略
