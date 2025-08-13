# 使用 autossh 自动重连 SSH

autossh 在 ssh 命令的基础上增加了自动重连功能，适用于需要长时间保持 SSH 连接的场景。

autossh 支持 ssh 命令中的所有选项，并增加如下额外的参数:

* `-M`: 指定监控端口，默认为 0，表示不使用监控。也可通过环境变量 `AUTOSSH_PORT` 设置。
  * port 和 port + 1 都会被使用，autossh 会在 SSH 连接内部建立一个反向端口转发（reverse port forwarding），将远程主机的 port 端口转发到本地的 port+1。如果测试数据发送失败，则会重新建立 SSH 连接。
* `-f`: 在后台运行（虽然 ssh 也有 `-f` 选项，但 autossh 会处理这个选项，并不会传递给 ssh）。

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

## 3 - 脚本封装

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
  autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 8080:localhost:80 user@remotehost
  ;;
 stop)
  killall -TERM autossh
  ;;
 restart)
  killall -TERM autossh
  autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 8080:localhost:80 user@remotehost
  ;;
 *)
  echo "Usage: $0 {start|stop|restart}"
  exit 1
  ;;
esac
exit 0
```
