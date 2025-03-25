# Go语言编译与工具

## go build命令

**【go build】指令的作用是：**在当前目录下编译生成可执行文件。

注意，go build指令会调用所有引用包的源码，重新编译，而不是直接使用pkg里的编译后文件，如果在【$GOROOT】与【$GOPATH】下没有找到import引入包的项目源码，就会报错。

【go build】会生成二进制文件到【$GOPATH/pkg/$GOOS_$GOARCH】目录下

### 无参数编译

如果源码中没有依赖 GOPATH 的包引用，那么这些源码可以使用无参数 go build。

```bash
go build
```

在代码所在目录下使用go build命令，命令会在编译开始时搜索当前目录的go源码，编译后生成可执行文件放到当前目录下，文件名与当前目录同名。

### go build + 文件列表

编译**同目录的**多个源码文件时，可以在 go build 的后面提供多个文件名，go build 会编译这些源码，输出可执行文件

```bash
go build file1.go file2.go……
```

使用“go build+文件列表”方式编译时，可执行文件默认选择文件列表中**第一个源码文件**作为可执行文件名输出。

如果需要指定输出可执行文件名，可以使用`-o`参数

```bash
# 指定输出可执行文件名为myexec
go build -o myexec main.go lib.go
```

### go build+包

在设置 `GOPATH` 后，可以直接根据包名进行编译，即便包内文件被增（加）删（除）也不影响编译指令。

```bash
export GOPATH=/home/davy/golangbook/code
go build -o main chapter11/goinstall
```

编译后可执行文件在包目录下。

注意：**源码必须放在 `GOPATH` 的 `src` 目录下。所有目录不要包含中文。**

### 编译时的附加参数

表中的附加参数按使用频率排列

| 附加参数 | 备  注                                      |
| -------- | ------------------------------------------- |
| -v       | 编译时显示包名                              |
| -p n     | 开启并发编译，默认情况下该值为 CPU 逻辑核数 |
| -a       | 强制重新构建                                |
| -n       | 打印编译时会用到的所有命令，但不真正执行    |
| -x       | 打印编译时会用到的所有命令                  |
| -race    | 开启竞态检测                                |

## go get

```bash
# 安装指定包
go get github.com/davyxu/cellnet
# 安装当前包所需的所有依赖
go get
```



```go

```

