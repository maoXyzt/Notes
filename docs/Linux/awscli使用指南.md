# awscli 使用指南

## 1. 安装和配置 awscli

检查是否有安装 awscli

```bash
aws --version
```

### 1.1 安装

参考官方文档: <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions>

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
# 如果 /usr/local/bin 不在 PATH 中，需要加入到 PATH
```

### 1.2 配置

配置 awscli 的默认配置:

```bash
aws configure
# 输入：
# AWS Access Key ID [None]: ************
# AWS Secret Access Key [None]: *********************************
# Default region name [None]: default
# Default output format [None]:
```

配置内容会写入 `~/.aws/credentials` 和 `~/.aws/config` 文件中。

配置默认 endpoint:

> [Configure endpoints using environment variables](https://docs.aws.amazon.com/sdkref/latest/guide/feature-ss-endpoints.html#ss-endpoints-envar)

```bash
export AWS_ENDPOINT_URL=http://localhost:4567
```

## 2. 操作

### 查询

*如有需要，可以手动指定 `--endpoint-url=http://endpoint.url.com` 来指定要访问的服务器*

```bash
# 列出所有 bucket
aws s3 ls
# 列出 bucket 的内容
aws s3 ls s3://myBucket
```

### 创建 bucket

```bash
aws s3 mb s3://myBucket
```

### 上传&下载

```bash
# upload
aws s3 cp myFolder/myFile.txt s3://myBucket/
# download
aws s3 cp s3://myBucket/myFile.txt myFolder/myFile.txt
```

### 同步

```bash
# 将本地目录同步到 myBucket 的 myFolder 前缀中
aws s3 sync . s3://myBucket/myFolder
# 将 myFolder 同步到 bucket 中，并在 bucket 中删除 myFolder 中没有的对象
aws s3 sync myFolder s3://myBucket/myFolder --delete
# 将非 txt 文件同步到 bucket 中
aws s3 sync . s3://myBucket --exclude "*.txt"
```

### 删除对象

```bash
aws s3 rm s3://myBucket/myFile.txt
```

### 删除 Bucket

```bash
aws s3 rb s3://myBucket
```

## 3. 权限控制

*如果配置的 endpoint 与默认的不一致，可以使用 `--endpoint-url=http://endpoint.url.com`*

### 上传策略

```bash
aws s3api put-bucket-policy --bucket <bucket-name> --policy file:///<path-to-file>
```

### 查询已有策略

```bash
aws s3api get-bucket-policy --bucket <bucket-name>
```

### 删除原有策略

```bash
aws s3api delete-bucket-policy --bucket <bucket-name>
```
