# docker 容器的 init 进程 (Tini)

> [Why do you need an init process inside your Docker container (PID 1)](https://daveiscoding.hashnode.dev/why-do-you-need-an-init-process-inside-your-docker-container-pid-1)

## 1 - 简介

[Tini](https://github.com/krallin/tini) 是一个用于在容器中运行进程的 init 进程。它提供了一些有用的功能，例如处理信号、自动处理僵尸进程和处理孤儿进程。

对于大多数应用而言，添加 Tini 并不需要对现有代码进行任何更改，它是完全透明的。

## 2 - 使用场景

### 2.1 处理信号

当你向容器发送信号 (`SIGINT` or `SIGTERM`) 时，Docker CLI 会将信号发送给容器内的 PID 1 进程。如果 PID 1 不是专门设计来处理信号的程序，那么这些信号可能不会被传递给应用程序本身，导致应用程序不能优雅地关闭。Tini 会接收这些信号并将它们转发给其子进程，确保容器内的应用程序能够正确响应这些信号。

### 2.2 自动处理僵尸进程

Tini 能够自动收割那些已经结束但尚未被父进程回收的僵尸进程。

## 3 - 如何使用

### 3.1 使用 `--init` 参数启动容器

`--init` 参数是 Docker (>=1.13) 提供的一个选项，用于在容器中运行一个 init 进程，通常是 [tini](https://github.com/krallin/tini)）作为 PID 1 进程。

不使用 `--init` 参数时:

```bash
docker run -it --rm ubuntu:16.04 /bin/bash
root@d740f7360840:/# ps -fA
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  1 03:30 ?        00:00:00 /bin/bash
root        11     1  0 03:30 ?        00:00:00 ps -fA
```

使用 `--init` 参数时:

```bash
docker run -it --init --rm ubuntu:16.04 /bin/bash
root@5b5fe6ee71b5:/# ps -fA
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  1 03:30 ?        00:00:00 /dev/init -- /bin/bash
root         7     1  0 03:30 ?        00:00:00 /bin/bash
root        12     7  0 03:30 ?        00:00:00 ps -fA
```

```bash
docker run --init -it --rm ubuntu:16.04 /bin/bash
```

### 3.2 显示指定 entrypoint

在 Dockerfile 中指定

```dockerfile
ENTRYPOINT ["/usr/local/bin/tini", "--"]
CMD ["your", "command", "here"]
```
