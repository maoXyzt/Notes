# 如何下载 golang.org 的包
>
> 作者：ppmoon
> 链接：<https://www.jianshu.com/p/096c5c253f75>
> 来源：简书

## 以下载 grpc 为例

grpc 官方提供的下载命令是：

```bash
go get google.golang.org/grpc
```

因为无法访问，所以我们需要在 `$GOPATH/src` 目录下面创建一个 `google.golang.org` 的目录。

在 github 上找到对应的 grpc 的包，[https://github.com/grpc/grpc-go](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fgrpc%2Fgrpc-go)，其实 [google.golang.org](https://link.jianshu.com?t=http%3A%2F%2Fgoogle.golang.org) 对应的就是 [https://github.com/grpc/grpc-go](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fgrpc%2Fgrpc-go)

然后我们进入到 `$GOPATH/src/google.golang.org` 这个目录。执行 git 命令

```bash
git clone --depth=1 https://github.com/grpc/grpc-go.git grpc
```

命令解析：

* 其中`--depth=1` 这个参数的意思是只克隆最新的 commit 分支。不加也行。
* 最后的 `grpc` 表示的是将克隆的文件存放到那个文件夹里面。
* 执行完上面的命令，我们就成功的将 `grpc` 的包下载到本地了。

```bash
go get google.golang.org/grpc
```

golang 当中 `go get` 其实执行了两个操作，一个是 `git clone` 另外一个 `go install`。

所以我们还要进入到 `$GOPATH/src/google.golang.org/grpc` 当中执行以下 `go install` 。

这个命令会在 `$GOPATH/pkg/google.golang.org/grpc` 下面生成一个 grpc.a 的外部包文件。用于和其他程序访问和编译。

并且在 `go install` 的过程当中我们可以检查哪些相关依赖的包没有安装，可以使用相同的办法进行安装。
