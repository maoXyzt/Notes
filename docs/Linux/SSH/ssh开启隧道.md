# SSH 开启隧道

> 如果需要自动重连 SSH 隧道，可以使用 [使用 autossh 自动重连 SSH](./使用autossh自动重连ssh.md)。

## 1 - 命令格式

```bash
ssh -g -N -L <local_port>:<remote_host_2>:<remote_port_2> <user>@<remote_host_1>
```

执行后，本机的 `<local_port>` 端口就会被映射到 `<remote_host_2>:<remote_port_2>`。

其他 host 也可以通过访问本机的 `<local_port>` 来访问 `<remote_host_2>:<remote_port_2>`。

## 2 - 参数说明

+ `-L`: 表示本地端口转发，指定本地 `<local_port>` 作为转发端口，将远程主机的端口 `<remote_host_2>:<remote_port_2>` 映射为本地端口
  + `[bind_address:]port:host:hostport`: <-- 常用
  + `[bind_address:]port:remote_socket`
  + `local_socket:host:hostport`
  + `local_socket:remote_socket`
+ `-R`: 与 `-L` 相对，表示将本地端口转发到远程主机
  + `[bind_address:]port:host:hostport`: <-- 常用
  + `[bind_address:]port:local_socket`
  + `remote_socket:host:hostport`
  + `remote_socket:local_socket`
+ `-g`: 允许外界主机连接本地转发端口 `<local_port>`
+ `-N`: 连接后不执行命令（否则隧道只在命令执行期间存在，命令完成后就会退出）
+ `-f`: 以后台方式运行
+ `<user>@<remote_host_1>`: 表示以 `<remote_host_1>` 作为隧道访问 `<remote_host_2>:<remote_port_2>`, `<user>` 为登录用户
  + 也使用可以在本机 `~/.ssh/config` 中配置的连接信息和别名

## 3 - Example

假设我们有一台主机可以 SSH 连接到 `fjscms` (在 `~/.ssh/config` 中已经配置了对 `fjscms` 的连接信息)，`fjscms` 可以访问到 `10.119.194.10` 的 `80` 端口。

我们在这台主机上通过 SSH 开启一个隧道，监听 `8080` 端口，访问这台主机的 `8080` 端口就可以访问到 `10.119.194.10:80`。

```bash
ssh -g -N -L 8080:10.119.194.10:80 fjscms
```
