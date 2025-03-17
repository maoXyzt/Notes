# git Error: Connection closed by 20.205.243.166 port 22

## 问题

执行git命令访问github时，出现如下错误：

```shell
Connection closed by 20.205.243.166 port 22
```

## 解决方法

配置使用https协议访问github，而不是ssh协议。

> Ref:
> [using-ssh-over-the-https-port](https://docs.github.com/en/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)

配置 `~/.ssh/config`, 添加如下内容：

```shell
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/id_rsa  # 可选
```

测试是否可以连接成功：

```shell
ssh -T git@github.com
# > Hi USERNAME! You've successfully authenticated, but GitHub does not
# > provide shell access.
```

### Updating known_hosts

See "[GitHub's SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)."
