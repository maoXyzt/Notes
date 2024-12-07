启动redis服务

```bash
redis-server /etc/redis/6379.conf	# 配置文件的路径
```

连接

```bash
redis-cli
# 如果修改了端口，则需要指定端口
redis-cli -p 6380
```

连接后

```bash
# 如设置了密码，输入密码进行验证
127.0.0.1:6379> auth password
OK
# 测试是否连通
127.0.0.1:6379> ping
PONG
# 切换库（默认是0号库）
127.0.0.1:6379> select 2
OK
127.0.0.1:6379[2]>
```

退出

```bash
127.0.0.1:6379> exit
```

