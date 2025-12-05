# 使用 autossh 自动重连 SSH

autossh 在 ssh 命令的基础上增加了自动重连功能，适用于需要长时间保持 SSH 连接的场景。

autossh 支持 ssh 命令中的所有选项，并增加如下额外的参数:

* `-M`: 指定监控端口，默认为 0，表示不使用监控。也可通过环境变量 `AUTOSSH_PORT` 设置。
  * port 和 port + 1 都会被使用，autossh 会在 SSH 连接内部建立一个反向端口转发（reverse port forwarding），将远程主机的 port 端口转发到本地的 port+1。如果测试数据发送失败，则会重新建立 SSH 连接。
* `-f`: 在后台运行（虽然 ssh 也有 `-f` 选项，但 autossh 会处理这个选项，并不会传递给 ssh）。

## 0 - TL;DR

**推荐命令：**

```bash
# 正向: 远程端口转发到本地
autossh -M 0 \
  -o "ServerAliveInterval=30" \
  -o "ServerAliveCountMax=3" \
  -o "ConnectTimeout=10" \
  -o "ExitOnForwardFailure=yes" \
  -N -L 8080:localhost:80 user@remotehost

# 反向: 本地端口转发到远程
autossh -M 0 \
  -o "ServerAliveInterval=30" \
  -o "ServerAliveCountMax=3" \
  -o "ConnectTimeout=10" \
  -o "ExitOnForwardFailure=yes" \
  -N -f -R 8080:localhost:80 user@remotehost
```

**参数说明：**

| 参数 | 用途 |
|-----|------|
| `-M 0` | 禁用 autossh 监控，使用 SSH 保活机制 |
| `ServerAliveInterval=30` | 每 30 秒发送保活包 |
| `ServerAliveCountMax=3` | 失败 3 次后断开 |
| `ConnectTimeout=10` | 连接超时 10 秒 |
| `ExitOnForwardFailure=yes` | 转发失败自动重连 |
| `-N` | 不执行远程命令 |
| `-f` | **后台运行** |
| `-L` | 本地端口转发（正向）|
| `-R` | 远程端口转发（反向）|

在 `8080:localhost:80` 中：

* `8080` = **本地监听端口**（执行命令的主机）
* `localhost:80` = **目标地址和端口**（远端服务地址）

**示例说明：**

```bash
# 正向转发 (-L): 在本地监听 8080，转发到远程的 80
# 访问本地 8080 就能访问远程主机上的 80 端口
-L 8080:localhost:80

# 反向转发 (-R): 在远程监听 8080，转发到本地的 80
# 从远程访问 localhost:8080 就能访问本地的 80 端口
-R 8080:localhost:80
```

**一键启动脚本：** 见第 5 章

## 1 - 安装 autossh

```bash
# Debian/Ubuntu
apt install autossh
# MacOS Homebrew
brew install autossh
```

验证安装结果 `autossh -V`

使用帮助 (输入 `autossh`):

```bash
usage: autossh [-V] [-M monitor_port[:echo_port]] [-f] [SSH_OPTIONS]

    -M specifies monitor port. Overrides the environment
       variable AUTOSSH_PORT. 0 turns monitoring loop off.
       Alternatively, a port for an echo service on the remote
       machine may be specified. (Normally port 7.)
    -f run in background (autossh handles this, and does not
       pass it to ssh.)
    -V print autossh version and exit.

Environment variables are:
    AUTOSSH_GATETIME    - how long must an ssh session be established
                          before we decide it really was established
                          (in seconds). Default is 30 seconds; use of -f
                          flag sets this to 0.
    AUTOSSH_LOGFILE     - file to log to (default is to use the syslog
                          facility)
    AUTOSSH_LOGLEVEL    - level of log verbosity
    AUTOSSH_MAXLIFETIME - set the maximum time to live (seconds)
    AUTOSSH_MAXSTART    - max times to restart (default is no limit)
    AUTOSSH_MESSAGE     - message to append to echo string (max 64 bytes)
    AUTOSSH_PATH        - path to ssh if not default
    AUTOSSH_PIDFILE     - write pid to this file
    AUTOSSH_POLL        - how often to check the connection (seconds)
    AUTOSSH_FIRST_POLL  - time before first connection check (seconds)
    AUTOSSH_PORT        - port to use for monitor connection
    AUTOSSH_DEBUG       - turn logging to maximum verbosity and log to
                          stderr
```

## 2 - 使用示例

### 2.1 将远程主机端口转发到本地

```bash
autossh -M 20000 -N -L 8080:localhost:80 user@:remote_host
```

其中:

* `-M` 指定 autossh 的监听端口。
* 其余参数与 `ssh` 命令相同，见 [SSH 开启隧道](./ssh开启隧道.md)

在本地访问 `8080` 端口就可以访问到远程主机的 `80` 端口。

### 2.1 将本地端口转发到远程主机

```bash
autossh -M 20000 -N -R 8080:localhost:80 user@:remote_host
```

其中:

* `-M` 指定 autossh 的监听端口。
* 其余参数与 `ssh` 命令相同，见 [SSH 开启隧道](./ssh开启隧道.md)

在远程主机上访问 `8080` 端口就可以访问到本地的 `80` 端口。

## 3 - 保活方案对比

### 3.1 `-M` 监控端口方案

脚本中使用 `-M 0` 结合 `ServerAliveInterval` 参数：

```bash
autossh -M 0 -o "ServerAliveInterval=30" -o "ServerAliveCountMax=3" -N -f -R 8080:localhost:80 user@remotehost
```

**关于 `-M 0` 参数：**

* `-M 0` 不是必须的，可以省略
* 如果不指定 `-M` 参数，autossh 会默认使用 `AUTOSSH_PORT` 环境变量（如果设置）
* 如果环境变量也未设置，autossh 会自动选择一个随机的监控端口进行反向转发监控
* 显式指定 `-M 0` 的作用是**明确禁用** autossh 的监控机制，完全依赖 SSH 的 `ServerAliveInterval` 保活

**行为对比：**

| 配置 | 保活机制 | 重连监控 |
|-----|--------|--------|
| `-M 0` | SSH `ServerAliveInterval` | autossh 进程监控 |
| 省略 `-M`（无环境变量） | SSH `ServerAliveInterval` + autossh 反向转发 | autossh 进程监控 + 反向转发测试 |
| 无参数 + 无保活参数 | 仅进程监控（无保活包） | autossh 反向转发 + 进程监控 |

**特点：**

* `-M 0` 禁用 autossh 的反向端口转发监控，由 SSH 本身的 `ServerAliveInterval` 机制保活
* `ServerAliveInterval=30` 每 30 秒发送一个保活包
* `ServerAliveCountMax=3` 失败 3 次后断开连接
* autossh 会监测 SSH 进程状态，进程异常则自动重启

**推荐场景：**

* 网络较稳定的环境
* 希望减少系统开销
* SSH 本身的保活机制足够满足需求

### 3.2 `-M` 监控端口 + 反向转发方案

```bash
autossh -M 20000 -N -f -R 8080:localhost:80 user@remotehost
```

**特点：**

* `-M 20000` 启用 autossh 监控，使用 20000 和 20001 端口进行反向端口转发
* autossh 主动发送测试数据验证连接，检测到连接断开立即重连
* 监控更灵敏，重连速度更快

**推荐场景：**

* 网络不稳定或容易掉线的环境
* 需要快速发现并恢复连接
* 对连接中断的容忍度低

### 3.3 选择建议

| 方案 | 网络稳定性 | 响应速度 | 系统开销 | 推荐度 |
|-----|---------|--------|--------|------|
| `-M 0 + ServerAliveInterval` | 一般 | 中等（30秒） | 低 | ⭐⭐⭐⭐ |
| `-M` 监控端口 | 差 | 快速（秒级） | 中等 | ⭐⭐⭐ |

**总体推荐：** `-M 0` + `ServerAliveInterval` 方案更优，原因：

1. 充分利用 SSH 内置的保活机制，更稳定可靠
2. 减少 autossh 和 SSH 之间的通信开销
3. 不需要额外占用监控端口
4. autossh 依然能通过进程监控实现自动重连

## 4 - 常用的 SSH 参数优化

除了基础的保活机制，还可以加入以下 SSH 参数进一步提升稳定性：

### 4.1 ConnectTimeout

```bash
-o "ConnectTimeout=10"
```

**作用：** 限制 SSH 连接超时时间为 10 秒

**必要性：** ⭐⭐⭐⭐⭐ （强烈推荐）

**原因：**

* 网络异常时可快速超时，避免长时间卡住
* autossh 检测到连接超时会立即重试
* 防止"僵尸"连接占用资源

### 4.2 ExitOnForwardFailure

```bash
-o "ExitOnForwardFailure=yes"
```

**作用：** 当端口转发失败时立即退出 SSH 连接

**必要性：** ⭐⭐⭐⭐ （推荐）

**原因：**

* 端口转发失败时自动断开（如远程端口被占用）
* autossh 检测到 SSH 退出会立即重连
* 避免占用连接却无法使用的情况
* 特别适合需要确保转发功能正常的场景

### 4.3 完整推荐配置

```bash
autossh -M 0 \
  -o "ServerAliveInterval=30" \
  -o "ServerAliveCountMax=3" \
  -o "ConnectTimeout=10" \
  -o "ExitOnForwardFailure=yes" \
  -N -f -R 8080:localhost:80 user@remotehost
```

## 5 - 脚本封装

```bash
#!/bin/bash
AUTOSSH_LOGFILE=/var/log/autossh.log
AUTOSSH_POLL=30
AUTOSSH_FIRST_POLL=60
AUTOSSH_GATETIME=0
AUTOSSH_PORT=0
AUTOSSH_DEBUG=yes
export AUTOSSH_LOGFILE AUTOSSH_POLL AUTOSSH_FIRST_POLL AUTOSSH_GATETIME AUTOSSH_PORT AUTOSSH_DEBUG
case "$1" in
 start)
  autossh -M 0 -o "ServerAliveInterval=30" -o "ServerAliveCountMax=3" -o "ConnectTimeout=10" -o "ExitOnForwardFailure=yes" -N -f -R 8080:localhost:80 user@remotehost
  ;;
 stop)
  killall -TERM autossh
  ;;
 restart)
  killall -TERM autossh
  autossh -M 0 -o "ServerAliveInterval=30" -o "ServerAliveCountMax=3" -o "ConnectTimeout=10" -o "ExitOnForwardFailure=yes" -N -f -R 8080:localhost:80 user@remotehost
  ;;
 *)
  echo "Usage: $0 {start|stop|restart}"
  exit 1
  ;;
esac
exit 0
```
