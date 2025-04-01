# Linux 环境变量设置：env, set, export

## 1 - `env` 命令

`env` 命令用于显示或设置环境变量。它可以在不启动新的 shell 的情况下运行命令，并传递环境变量。

显示所有环境变量

```bash
env
```

显示指定环境变量

```bash
env | grep PATH
```

设置当前系统中的指定环境变量值

```bash
env VAR_NAME=value
```

删除当前系统中的指定环境变量

```bash
env -u VAR_NAME
```

## 2 - `set` 命令

`set` 命令用于设置 shell 的环境变量和选项。它可以显示当前 shell 的所有变量和函数。

在 bash 中，`set` 命令的行为与 `env` 命令略有不同。它会显示所有变量，包括 shell 函数和位置参数。

显示所有变量和函数

```bash
set
```

显示指定变量

```bash
set | grep PATH
```

## 3 - `export` 命令

`export` 可新增，修改或删除环境变量，供后续执行的程序使用。export 的效力仅限于该次登陆操作。

列出所有环境变量

```bash
export -p
```

定义环境变量

```bash
export VAR_NAME
```

设置环境变量值

```bash
export VAR_NAME=value
```
