# 使用 OpenSSL 生成自签名 SSL 证书

> <https://blog.csdn.net/nklinsirui/article/details/89432430>

## 0. 检查 OpenSSL

```bash
openssl version
```

## 1. 生成私钥

```bash
# genra 生成 RSA 私钥
# -des3 des3 算法
# -out server.key 生成的私钥文件名
# 2048 私钥长度
openssl genrsa -des3 -out server.pass.key 2048
```

输入一个 4 位以上的密码。

## 2. 去除私钥中的密码

```bash
openssl rsa -in server.pass.key -out server.key
```

> 注意：有密码的私钥是 server.pass.key，没有密码的私钥是 server.key

## 3. 生成 CSR(证书签名请求)

```bash
# req 生成证书签名请求
# -new 新生成
# -key 私钥文件
# -out 生成的 CSR 文件
# -subj 生成 CSR 证书的参数
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Guangdong/L=Guangzhou/O=xdevops/OU=xdevops/CN=gitlab.xdevops.cn"
```

subj 参数说明如下：

| 字段 | 字段含义 | 示例 |
| ---- | -------- | ---- |
| /C =  | Country 国家 | CN |
| /ST = | State or Province 省 | Guangdong |
| /L = | Location or City 城市 |  Guangzhou |
| /O = | Organization 组织或企业 | xdevops |
| /OU = | Organization Unit 部门 | xdevops |
| /CN = | Common Name 域名或 IP | gitlab.xdevops.cn |

## 4. 生成自签名 SSL 证书

```bash
# -days 证书有效期
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

> X.509 证书包含三个文件：key，csr，crt。
>
> - key 是服务器上的私钥文件，用于对发送给客户端数据的加密，以及对从客户端接收到数据的解密
> - csr 是证书签名请求文件，用于提交给证书颁发机构（CA）对证书签名
> - crt 是由证书颁发机构（CA）签名后的证书，或者是开发者自签名的证书，包含证书持有人的信息，持有人的公钥，以及签署者的签名等信息
>
> 备注：在密码学中，X.509 是一个标准，规范了公开秘钥认证、证书吊销列表、授权凭证、凭证路径验证算法等。

## 5. 在 Server 中配置

在 Server 中配置：

- 声明开启 HTTPS (SSL 认证)
- 声明侦听 443 端口（并确保已在防火墙上打开 443 端口）
- 复制已签名的 SSL 证书和私钥到指定位置，并设置正确的文件权限
- 配置已签名的 SSL 证书（.crt）的位置
- 配置已签名的 SSL 证书私钥（.key）的位置
- 配置将 HTTP 请求都重定向到 HTTPS
