# awscli 使用指南

## 1. 安装和配置awscli

检查是否有安装 awscli

```bash
aws --version
```

### 安装

略。

建议`python>=3.7`

### 配置

(1) `vim ~/.s3cfg`

```conf
[default]
access_key = 111
secret_key = 222
host_base = http://10.5.41.12:7480
host_bucket = http://10.5.41.12:7480/%(bucket)
```

(2) `aws configure`

输入 access_key 和 secret_key

## 2. 操作

### 查询

*有时需要加上`--endpoint-url=http://endpoint.url.com`来指定要访问的服务器*

```bash
# 列出所有bucket
aws s3 ls
# 列出bucket的内容
aws s3 ls s3://myBucket
```

### 创建bucket

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
# 将本地目录同步到myBucket的myFolder前缀中
aws s3 sync . s3://myBucket/myFolder
# 将myFolder同步到bucket中，并在bucket中删除myFolder中没有的对象
aws s3 sync myFolder s3://myBucket/myFolder --delete
# 将非txt文件同步到bucket中
aws s3 sync . s3://myBucket --exclude "*.txt"
```

### 删除对象

```bash
aws s3 rm s3://myBucket/myFile.txt
```

### 删除Bucket

```bash
aws s3 rb s3://myBucket
```

## 3. 权限控制

*如果配置的endpoint与默认的不一致，可以使用`--endpoint-url=http://endpoint.url.com`*

### 上传策略

```bash
aws s3api put-bucket-policy --bucket <bucket-name> --policy file:///<path-to-file>
```

、

### 查询已有策略

```bash
aws s3api get-bucket-policy --bucket <bucket-name>
```

### 删除原有策略

```bash
aws s3api delete-bucket-policy --bucket <bucket-name>
```
