## 新增用户
```bash
# useradd -d <USERHOME> -m <USERNAME> # 指定用户主目录，如果此目录不存在，则同时使用-m选项，可以创建主目录
useradd -m user1
passwd user1  				# 设置密码
chsh -s /bin/bash user1 	# 登陆后使用bash
```

## 创建密码
```bash
passwd 账号
```
## 赋予用户sudo权限列表
Linux默认是没有将用户添加到sudoers列表中的，需要root手动将账户添加到sudoers列表中，才能让普通账户执行sudo命令。

root 账户下输入`visudo`或`vim /etc/sudoers`，找到如下语句：
```
root    ALL=(ALL)       ALL
```
按yyp键复制并在粘贴在下一行，在这一行的 root替换为你所需要添加用户的账户名，比如huddy，结果就是
```
root    ALL=(ALL)       ALL
huddy  ALL=(ALL)       ALL
```

如果你希望之后执行sudo命令时不需要输入密码，那么可以形如
```
root    ALL=(ALL)       ALL
huddy  ALL=(ALL)       NOPASSWD:ALL
```

## 赋予用户SSH连接的权限
linux系统安装好，建立普通用户后，普通用户不一定能通过ssh连接到服务器

可以在/etc/ssh/sshd_config中增加`AllowUsers:username`(可以多个,空格分开)给普通用户增加ssh权限

也可以设置允许和拒绝ssh的用户/用户组：
```
DenyUsers:username,DenyGroups:groupname
```

优先级如下:

    DenyUsers:username
    AllowUsers:username
    DenyGroups:groupname
    AllowGroups:groupname

在给普通用户设立ssh权限后，即可将root ssh权限禁用，增加安全性

（也可以在sshd_config中将PermitRootLogin 选项修改为:PermitRootLogin no）
