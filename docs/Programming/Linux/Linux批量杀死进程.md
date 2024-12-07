如下：

```bash
ps -efww|grep supervisord.conf|grep -v grep|cut -c 9-15|xargs kill -9
```

```bash
ps -ef|grep supervisord.conf|grep -v grep|awk "{print $2}"|xargs kill -9
```

