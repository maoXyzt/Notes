# Linux 新建用户，赋予 sudo 权限，并允许 ssh 连接

## 1. 新增用户

命令如下:

```bash
useradd -m user1
chsh -s /bin/bash user1  # 登陆后使用 bash
passwd user1      # 设置密码
# <根据提示输入密码>
```

命令说明:

```bash
useradd -m [-d <USERHOME>] <USERNAME>
```

* `-d`: (可选) 不使用默认主目录，指定用户主目录。如果此目录不存在，则必须使用 `-m` 选项创建主目录，否则这个用户将无法登录。
* `-m`: 创建用户主目录
* `<USERNAME>`: 用户名

例如，同时指定UID、用户名、用户组、用户主目录:

```bash
groupadd -g 1001 user1
useradd -u 1001 -g 1001 -d "/home/user1" -m user1
```

## 2. 赋予用户 sudo 权限列表

Linux 默认是没有将用户添加到 sudoers 列表中的，需要 root 手动将账户添加到 sudoers 列表中，才能让普通账户执行 sudo 命令。

root 账户下输入 `visudo`，（不建议使用 `vim /etc/sudoers`，因为该文件是只读的）找到如下语句：

> 可以用 `VISUAL` 环境变量指定 `visudo` 的使用的编辑器，比如 `VISUAL=vim visudo`

```bash
# User privilege specification
root    ALL=(ALL:ALL) ALL
```

按 `yyp` 键复制并在粘贴在下一行，在这一行的 `root` 替换为你所需要添加用户的账户名，比如 `huddy`，结果就是

```bash
# User privilege specification
root    ALL=(ALL:ALL) ALL
huddy   ALL=(ALL:ALL) ALL
```

如果你希望之后执行 sudo 命令时不需要输入密码，那么可以形如

```bash
# User privilege specification
root    ALL=(ALL:ALL) ALL
huddy   ALL=(ALL:ALL) NOPASSWD:ALL
```

## 3. 赋予用户 SSH 连接的权限

linux 系统安装好，建立普通用户后，普通用户不一定能通过 ssh 连接到服务器

可以在 `/etc/ssh/sshd_config` 中增加 `AllowUsers:username`(可以多个, 空格分开)给普通用户增加 ssh 权限

也可以设置允许和拒绝 ssh 的用户/用户组：

```bash
DenyUsers:username,DenyGroups:groupname
```

优先级如下:

1. DenyUsers: username
2. AllowUsers: username
3. DenyGroups: groupname
4. AllowGroups: groupname

在给普通用户赋予 ssh 权限后，可将 root ssh 权限禁用，增加安全性

（也可以在 `sshd_config` 中将 `PermitRootLogin` 选项修改为: `PermitRootLogin no`)
