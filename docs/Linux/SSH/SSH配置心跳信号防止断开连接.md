# SSH 配置心跳信号防止断开连接

## 在客户端进行配置

客户端保活

`~/.ssh/config`

```bash
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 2
```

+ `ServerAliveInterval` 设置为 60 秒，意味着每分钟你的 SSH 客户端会向服务器发送一个“心跳”消息，这样即使你在本地没有任何活动，也会让服务器知道你仍然在线。
+ `ServerAliveCountMax` 设置为 2，则表示如果连续两次心跳都没有得到响应，连接将会被关闭。

## 在服务端配置

编辑 `/etc/ssh/sshd_config`，找到如下配置项，取消注释并设置：

```bash
ClientAliveInterval 60
ClientAliveCountMax 3
```

它表示 SSH 服务器每隔 60 秒向客户端发送一次请求，若连续 3 次没有收到回复，则自动断开连接。

重启 sshd 使设置生效

```bash
service sshd restart
```

## 针对单次连接设置

```bash
ssh -o ServerAliveInterval=30 user@host
```
