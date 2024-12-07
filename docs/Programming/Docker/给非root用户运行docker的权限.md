# 给非root用户运行docker命令的权限

## 方法: 创建名为docker用户组

docker守护进程启动的时候，会默认赋予名为docker的用户组读写Unix socket的权限，因此只要创建docker用户组，并将当前用户加入到docker用户组中，那么当前用户就有权限访问Unix socket了，进而也就可以执行docker相关命令

```bash
sudo groupadd docker	# 创建docker用户组
sudo gpasswd -a $USER docker  # 将当前登录用户加入到docker用户组中
newgrp docker	# 更新用户组
```

命令说明：

1. `groupadd`命令：新建用户组

2. `gpasswd`命令：管理组

   > 其实 gpasswd 命令是用来设定组密码并指定组管理员的，不过组密码和组管理员功能很少使用，而且完全可以被 sudo 命令取代，所以 gpasswd  命令现在主要用于把用户添加进组或从组中删除。

   - -a：添加用户到组
   - -d：从组删除用户
   - -A：指定管理员
   - -M：指定组成员和-A的用途差不多
   - -r：删除密码
   - -R：限制用户登入组，只有组中的成员才可以用newgrp加入该组

3. `newgrp`命令：登入另一个群组
