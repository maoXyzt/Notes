# TCP & UDP 端口连通性测试

## TCP 端口测试

`telnet` 命令：Linux & windows 都可以使用

```bash
telnet 192.168.209.121 123
```

## UDP 端口测试

`nc` 命令

```bash
nc -vuz 192.168.209.121 123
```

实际使用时可以只用-u参数。-u代表udp协议 ，-v代表详细模式，-z代表只监测端口不发送数据。
