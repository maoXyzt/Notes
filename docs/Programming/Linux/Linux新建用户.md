# Linux 新建用户

## 新增用户

```bash
# useradd -d <USERHOME> -m <USERNAME> # 指定用户主目录，如果此目录不存在，则同时使用-m 选项，可以创建主目录
useradd -m user1
passwd user1      # 设置密码
chsh -s /bin/bash user1  # 登陆后使用 bash
```

## 创建密码

```bash
passwd 账号
```

## 赋予用户 sudo 权限列表

Linux 默认是没有将用户添加到 sudoers 列表中的，需要 root 手动将账户添加到 sudoers 列表中，才能让普通账户执行 sudo 命令。

root 账户下输入 `visudo` 或 `vim /etc/sudoers`，找到如下语句：

```bash
root    ALL=(ALL)       ALL
```

按 yyp 键复制并在粘贴在下一行，在这一行的 root 替换为你所需要添加用户的账户名，比如 huddy，结果就是

```bash
root    ALL=(ALL)       ALL
huddy  ALL=(ALL)       ALL
```

如果你希望之后执行 sudo 命令时不需要输入密码，那么可以形如

```bash
root    ALL=(ALL)       ALL
huddy  ALL=(ALL)       NOPASSWD:ALL
```

## 赋予用户 SSH 连接的权限

linux 系统安装好，建立普通用户后，普通用户不一定能通过 ssh 连接到服务器

可以在/etc/ssh/sshd_config 中增加 `AllowUsers:username`(可以多个, 空格分开)给普通用户增加 ssh 权限

也可以设置允许和拒绝 ssh 的用户/用户组：

```bash
DenyUsers:username,DenyGroups:groupname
```

优先级如下:

1. DenyUsers: username
2. AllowUsers: username
3. DenyGroups: groupname
4. AllowGroups: groupname

在给普通用户设立 ssh 权限后，即可将 root ssh 权限禁用，增加安全性

（也可以在 sshd_config 中将 PermitRootLogin 选项修改为: PermitRootLogin no）
