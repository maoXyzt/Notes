# 创建 SSH 密钥对并使用密钥登录

## 1 - 使用 ssh-keygen 命令生成密钥对

执行 `ssh-keygen` 命令，获取私钥证书 `id_rsa` 和公钥证书 `id_rsa.pub`

```bash
# 使用 Ed25519 算法生成密钥对, 要求 OpenSSH 6.5 及以上版本(2014 年)
ssh-keygen -t ed25519 -b 256 -C "example@qq.com"
# 如果 OpenSSH 版本低于 6.5, 也可使用 rsa 算法生成 2048 位密钥对 (默认) ：
# ssh-keygen -C "example@qq.com"

Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):   # <- 直接输入回车(设置访问密钥需要的短文密码，一般不设置)
Enter same passphrase again:                  # <- 直接输入回车
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
```

`ssh-keygen` 参数说明:

- `-t` 指定密钥类型, 默认是 rsa。
- `-C` 设置注释文字, 比如邮箱、主机名，方便识别。
- `-b` 指定密钥长度。对于 RSA 密钥，最小要求 768 位，默认是 2048 位。DSA 密钥必须恰好是 1024 位(FIPS 186-2 标准的要求)。
- `-f` 指定密钥文件存储文件名。

## 2 - 配置登录密钥

用 `ssh-copy-id` 把公钥复制到远程主机上

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.0.3
# 输入密码
```

注：`ssh-copy-id` 会把公钥追加到远程主机的 `.ssh/authorized_key` 上

> 也可以手动把公钥内容添加到远程主机的 `~/.ssh/authorized_key` 文件

## 3 - 关于 Ed25519 算法

Ed25519 是一种基于 椭圆曲线密码学 (ECC) 的非对称加密算法，专门用于数字签名和密钥交换。

它由 Daniel J. Bernstein 等人在 2011 年提出，基于 Edwards 曲线 (Edwards Curve)的一种特定形式 (Ed25519) 。其核心特性包括：

- 安全性：基于椭圆曲线密码学 (ECC) ，提供 128 位安全性，抗量子计算攻击能力更强。
- 密钥长度：固定使用 256 位密钥，公钥和私钥尺寸更小。
- 性能：签名和验证速度比 RSA 快得多，尤其适合资源受限的设备 (如嵌入式系统、物联网设备) 。
- 应用场景：广泛用于 SSH、TLS、区块链 (如 Monero、Nano) 、加密通信协议 (如 Signal) 等。

### Ed25519 与 RSA 的对比

| 特性     | Ed25519                                              | RSA                                                 |
| -------- | ---------------------------------------------------- | --------------------------------------------------- |
| 算法基础 | 基于椭圆曲线密码学 (ECC)                             | 基于大整数分解难题 (Factorization Problem)          |
| 安全性   | 更高 (256 位密钥 ≈ 3072 位 RSA 的安全性)             | 高 (依赖密钥长度，2048/4096 位)                     |
| 密钥长度 | 固定 256 位 (私钥/公钥更短)                          | 通常 2048/4096 位 (公钥较大)                        |
| 性能     | 更快 (签名/验证速度远超 RSA，尤其适合高并发场景)     | 较慢 (4096 位 RSA 的签名和验证速度显著低于 Ed25519) |
| 密钥尺寸 | 公钥和私钥尺寸更小 (适合低带宽环境)                  | 密钥尺寸较大 (占用更多存储和传输资源)               |
| 兼容性   | 需 OpenSSH 6.5+ 及较新系统支持 (部分老旧系统不兼容)  | 几乎所有系统支持 (兼容性最佳)                       |
| 推荐场景 | 现代系统、高性能需求、资源受限设备 (如 IoT)          | 遗留系统、需广泛兼容性 (如旧版 SSH 客户端)          |

### 为什么推荐 Ed25519 而不是 RSA？

- 安全性更高
  - Ed25519 的 256 位密钥与 RSA 的 3072 位密钥安全性相当，但密钥长度更短。
  - ECC 抗量子计算攻击的能力优于 RSA (未来抗量子计算威胁更优) 。
- 性能更优
  - Ed25519 的签名和验证速度比 RSA 快数倍，尤其适合高并发场景 (如 SSH 登录、API 调用) 。
  - 在资源受限设备 (如 IoT) 中，ED25519 的低计算开销更实用。
  - Ed25519 公钥仅 64 字节，而 RSA 4096 位公钥约 512 字节，传输和存储成本更低。
- 现代标准趋势
  - TLS/SSL、SSH、区块链等现代协议已广泛采用 Ed25519 (如 OpenSSH 6.5+ 默认支持) 。
  - RSA 因安全性和性能劣势逐渐被淘汰。

### 如何选择？

优先选择 ED25519：

- 如果你的系统支持 Ed25519 (如 OpenSSH 6.5+) ，且无需兼容老旧系统，ED25519 是更安全、高效的首选。
- 选择 RSA 的场景：
  - 如果你需要兼容老旧系统 (如旧版 SSH 客户端) ，或某些行业标准强制要求 RSA，则继续使用 RSA (推荐密钥长度 3072 位或更高) 。

## 4 - 有多个密钥文件时如何使用

### 4.1 SSH 的默认密钥优先级

SSH 客户端默认会按以下顺序尝试加载密钥 (按算法优先级排序) ：

- id_rsa (RSA 算法)
- id_ecdsa (ECDSA 算法)
- id_ed25519 (Ed25519 算法)

因此，如果没有显式配置，SSH 会优先使用 id_rsa (RSA 密钥) ，即使 id_ed25519 存在。

### 4.2 如何强制使用特定密钥？

#### 方法 1：通过 `~/.ssh/config` 文件配置

你可以通过编辑 ~/.ssh/config 文件，为特定主机指定使用的密钥。例如：

```bash
# ~/.ssh/config
Host example.com
    HostName example.com
    User your_username
    IdentityFile ~/.ssh/id_ed25519  # 强制使用 Ed25519 密钥
```

说明：

- `Host example.com` 表示该配置仅对 example.com 生效。
- `IdentityFile` 指定使用的私钥路径。

#### 方法 2：通过命令行参数指定

在连接时，使用 `-i` 参数显式指定私钥文件：

```bash
ssh -i ~/.ssh/id_ed25519 <user@example.com>
```

说明：

- 该方法会覆盖默认行为，强制使用指定的密钥。

#### 方法 3：通过 `ssh-add` 添加到 SSH 代理

如果使用 ssh-agent 管理密钥，可以通过 `ssh-add` 指定默认使用的密钥：

```bash
# 添加 Ed25519 密钥到代理
ssh-add ~/.ssh/id_ed25519

# 查看当前代理中的密钥
ssh-add -l
```

说明：

- ssh-agent 会优先使用最近添加的密钥，但如果你同时添加了多个密钥，SSH 会根据算法优先级选择。

### 4.3 验证当前使用的密钥

你可以通过以下方式确认 SSH 使用的密钥：

#### 方法 1：使用 `-v` 参数查看详细日志

```bash
ssh -v <user@example.com>
```

在输出中查找类似以下内容：

```bash
debug1: Offering public key: /home/user/.ssh/id_ed25519
# 这表示 SSH 使用了 id_ed25519。
```

#### 方法 2：检查 `~/.ssh/authorized_keys`

确保目标服务器的 `~/.ssh/authorized_keys` 文件中包含你希望使用的公钥 (例如 id_ed25519.pub 的内容) 。

## 4 - 注意事项

### 4.1 权限问题

确保 `~/.ssh` 目录权限为 `700` (`chmod 700 ~/.ssh`) 。
私钥文件 (如 id_rsa、id_ed25519) 权限应为 `600` (`chmod 600 ~/.ssh/id_rsa`) 。

- 如果权限过松，SSH 会拒绝使用密钥。
