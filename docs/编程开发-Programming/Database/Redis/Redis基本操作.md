# Redis 基本操作

## 1. 启动 redis 服务

```bash
redis-server /etc/redis/6379.conf # 配置文件的路径
```

## 2. redis-cli 命令

### 2.1 连接 redis 服务

```bash
redis-cli
# 如果修改了端口，则需要指定端口
redis-cli -p 6380
```

### 2.2 常用命令

#### 验证密码

如果设置了密码，通过 `auth` 命令进行验证

```bash
127.0.0.1:6379> auth your_password
OK
```

#### 测试是否连通

```bash
127.0.0.1:6379> ping
PONG
```

#### 切换库（默认是 0 号库）

```bash
127.0.0.1:6379> select 2
OK
127.0.0.1:6379[2]>
```

#### 退出

```bash
127.0.0.1:6379> exit
```
