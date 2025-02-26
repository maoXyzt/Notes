# 给非 root 用户运行 docker 命令的权限

> [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

## 方法: 创建名为 docker 用户组

docker 守护进程启动的时候，会默认赋予名为 docker 的用户组读写 Unix socket 的权限，因此只要创建 docker 用户组，并将当前用户加入到 docker 用户组中，那么当前用户就有权限访问 Unix socket 了，进而也就可以执行 docker 相关命令

```bash
# 创建 docker 用户组
sudo groupadd docker
# 将当前登录用户加入到 docker 用户组中
sudo usermod -aG docker $USER
# 更新用户组, 使用户组生效; 或者注销重新登录
newgrp docker
```

命令说明：

1. `groupadd` 命令：新建用户组

2. `usermod` 命令：管理组
   + 使用-G将用户附加到其他组，可以与-a参数联合使用，表示追加一个附加组。

3. `newgrp` 命令：登入另一个群组
