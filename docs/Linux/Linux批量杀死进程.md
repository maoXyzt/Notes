# Linux 批量杀死进程

命令如下：

```bash
ps -efww | grep supervisord.conf | grep -v grep | cut -c 9-15 | xargs kill -9
```

```bash
ps -ef | grep supervisord.conf | grep -v grep | awk "{print $2}" | xargs kill -9
```

区别是 `cut -c 9-15` 和 `awk "{print $2}"`，前者是截取第 9 到 15 个字符，后者是打印第 2 列。目的都是获取进程号。
