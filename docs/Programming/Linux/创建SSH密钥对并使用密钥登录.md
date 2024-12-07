## 使用ssh-keygen命令生成密钥对

执行 `ssh-keygen` 命令，获取私钥证书`id_rsa`和公钥证书`id_rsa.pub`

```bash
ssh-keygen -t rsa -C "example@qq.com"

Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase): <-- 直接输入回车(设置访问密钥需要的短文密码，一般不设置)
Enter same passphrase again: <-- 直接输入回车
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
```

`ssh-keygen` 参数说明

> -t 指定密钥类型,默认是 rsa,可以省略.
>
> -C 设置注释文字,比如邮箱.
>
> -b 指定密钥长度。对于RSA密钥，最小要求768位，默认是2048位。DSA密钥必须恰好是1024位(FIPS 186-2 标准的要求)。
>
> -f 指定密钥文件存储文件名.

## 配置使用密钥登录

用 `ssh-copy-id` 把公钥复制到远程主机上

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.0.3
# 输入密码
```

注：`ssh-copy-id` 会把公钥追加到远程主机的 `.ssh/authorized_key` 上

> 也可以手动把公钥内容添加到远程主机的 `~/.ssh/authorized_key` 文件

