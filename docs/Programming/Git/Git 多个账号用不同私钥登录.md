## 0. 场景

Git报错：

> ERROR: Permission to XXX.git denied to user

这是因为 Github 不允许多个账号用同一个密钥登录，在同一台电脑上想要多个账号都免密登录时，需要配置不同的账号使用不同的私钥。

## 1. 生成新的SSH key

假设新生成的密钥对为：

- `id_rsa2`
- `id_rsa2.pub`

将公钥内容添加到 GitHub 后台

## 2. 配置Host别名

编辑 `~/.ssh/config` 文件

在不影响默认的 github 设置下我们重新添加一个 Host ，另取一个名称，如 github-user2：

```config
# 默认的，不需要添加
# Host github.com
# HostName github.com
# User git
# IdentityFile ~/.ssh/id_rsa

Host github-user2
HostName github.com
User git
IdentityFile ~/.ssh/id_rsa2		# 私钥位置
```

## 3. 修改 GitHub SSH 仓库地址使用 Host 别名

如原地址是：

`git@github.com:hbxn740150254/BestoneGitHub.git` 

替换后应该是：

`git@github-user2:hbxn740150254/BestoneGitHub.git` 
或者
`github-user2:hbxn740150254/BestoneGitHub.git`

## PS: github账户如果还是显示之前id_rsa密钥账户

### 添加你的ssh密钥到ssh-agent中

```bash
# start the ssh-agent in the background
eval "$(ssh-agent -s)"
Agent pid 59566
```

如果你的密钥不是系统默认的RSA文件名 id_rsa 比如创了一对公钥/密钥id_rsa_personal，那么就把它们添加进去，注意：密钥文件是不带扩展名的，公钥扩展名是.pub，代表publicKey

```bash
$ eval "$(ssh-agent -s)"
Agent pid 19795
//添加密钥 id_rsa_personal
$ ssh-add id_rsa_personal
Identity added: id_rsa_personal (github-personal)
//添加默认密钥 id_rsa
$ ssh-add id_rsa
//密钥有密码的话就会要你提示输入 passphrase
Enter passphrase for id_rsa: 
//测试用密钥isa是否连接成功github
$ ssh -T git@github.com
Hi hbxn740150254! You 've successfully authenticated, but GitHub does not provide shell access.
//测试密钥id_rsa_personal是否连接成功github
$ ssh -T git@github-personal
Hi FaxeXian! You've successfully authenticated, but GitHub does not provide shell access.
```
