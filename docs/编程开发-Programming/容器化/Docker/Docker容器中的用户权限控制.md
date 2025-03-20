# Docker 容器中的权限控制

## 1. 默认使用 root 权限

不管是以root用户还是以普通用户（有启动docker容器的权限）启动docker容器，**容器进程和容器内**的用户权限都是root。

## 2. 限制 Docker 容器启动时的用户

在Dockerfile中，如果指定了`USER`参数，或者使用`--user`参数启动容器：

```bash
docker run --user user_name_or_uid xxxxxxx
```

会发现容器中的uid号和宿主机中的uid号一样，也验证了docker容器使用宿主机的内核。

## 3. 使用 namespace 隔离技术

TODO:
