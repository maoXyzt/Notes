# Linux 修改默认shell

## 修改用户的默认shell

查看所有 shell

```bash
chsh -l
```

如果你没有管理员权限, 那么你只能修改自己的 Shell, 输入 chsh 命令.

```bash
chsh
```

这时你会获得提醒, 要求输入新的 Shell 应用路径. 如果你要换成 bash, 请输入 /bin/bash 并回车确认.

```bash
Enter the new value, or press ENTER for the default
Login Shell [/bin/sh]:
```

如果你是管理员, 那么除了使用 chsh 命令, 你还可以通过修改配置文件批量修改.

```bash
vi /etc/passwd
```

打开 /etc/passwd 文件, 你将看到所有用户及其使用的 Shell, 会有很多行类似这样的内容, 每行是一个用户.

```bash
zhao.wuz:x:1003:33::/home/zhao.wuz:/bin/sh
```

这里只需要件 /bin/sh 改成 /bin/bash 即可.

## 添加用户时指定Shell

在添加用户时可以通过以下命令指定 Shell.

```bash
useradd -s /bin/bash {用户名}
```
