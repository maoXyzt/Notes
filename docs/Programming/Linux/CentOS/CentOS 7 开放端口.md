# CentOS 7 防火墙开放端口

## 1. 添加开放对外的端口

```bash
firewall-cmd --zone=public --add-port=8080/tcp --permanent
```

参数含义：

- `--zone`: 作用域
- `add-port`: 添加端口，格式为：<端口>/<通讯协议>
- `permanent`: 永久生效，没有此参数则重启后失效

## 2. 重启防火墙

```bash
firewall-cmd --reload
```

## 3. 查看已经对外开放的端口

```bash
firewall-cmd --list-ports
```

## 4. 其他相关命令

防火墙相关命令

```bash
# 开启防火墙
systemctl start firewalld
# 关闭防火墙
systemctl stop firewalld
# 重启防火墙服务
systemctl restart firewalld.service
# 查看当前防火墙状态
firewall-cmd --state
# 禁止开机启动
systemctl disable firewalld.service
```

查看监听的端口

```bash
netstat -lntp
```

检查端口被哪个进程占用

```bash
# 方法 1
netstat -lnp|grep 8080
# 方法 2
lsof -i :8080
```

删除端口配置

```bash
firewall-cmd --zone= public--remove-port=80/tcp --permanent
```

测试端口（DOS 中）

```bash
telnet xxx.xxx.xxx.xxx:pppp
```
