# 使用OpenSSL生成自签名SSL证书

> https://blog.csdn.net/nklinsirui/article/details/89432430

## 0. 检查OpenSSL

```bash
openssl version
```

## 1. 生成私钥

```bash
# genra	生成RSA私钥
# -des3	des3算法
# -out server.key 生成的私钥文件名
# 2048 私钥长度
openssl genrsa -des3 -out server.pass.key 2048
```

输入一个4位以上的密码。

## 2. 去除私钥中的密码

```bash
openssl rsa -in server.pass.key -out server.key
```

> 注意：有密码的私钥是server.pass.key，没有密码的私钥是server.key

## 3. 生成CSR(证书签名请求)

```bash
# req 生成证书签名请求
# -new 新生成
# -key 私钥文件
# -out 生成的CSR文件
# -subj 生成CSR证书的参数
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Guangdong/L=Guangzhou/O=xdevops/OU=xdevops/CN=gitlab.xdevops.cn"
```

subj参数说明如下：

| 字段 | 字段含义 | 示例 |
| ---- | -------- | ---- |
| /C=  | Country 国家 | CN |
| /ST= | State or Province 省 | Guangdong |
| /L= | Location or City 城市 |  Guangzhou |
| /O= | Organization 组织或企业 | xdevops |
| /OU= | Organization Unit 部门 | xdevops |
| /CN= | Common Name 域名或IP | gitlab.xdevops.cn |

## 4. 生成自签名SSL证书

```bash
# -days 证书有效期
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

> X.509证书包含三个文件：key，csr，crt。
>
> - key是服务器上的私钥文件，用于对发送给客户端数据的加密，以及对从客户端接收到数据的解密
> - csr是证书签名请求文件，用于提交给证书颁发机构（CA）对证书签名
> - crt是由证书颁发机构（CA）签名后的证书，或者是开发者自签名的证书，包含证书持有人的信息，持有人的公钥，以及签署者的签名等信息
>
> 备注：在密码学中，X.509是一个标准，规范了公开秘钥认证、证书吊销列表、授权凭证、凭证路径验证算法等。

## 5. 在Server中配置

在Server中配置：

- 声明开启HTTPS (SSL认证)
- 声明侦听443端口（并确保已在防火墙上打开443端口）
- 复制已签名的SSL证书和私钥到指定位置，并设置正确的文件权限
- 配置已签名的SSL证书（.crt）的位置
- 配置已签名的SSL证书私钥（.key）的位置
- 配置将HTTP请求都重定向到HTTPS