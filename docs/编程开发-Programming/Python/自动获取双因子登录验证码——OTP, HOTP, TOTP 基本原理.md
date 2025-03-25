# 自动获取双因子登录验证码: OTP, HOTP, TOTP 基本原理

## 1 - 双因子(2FA)登录验证码原理

### 1.1 什么是双因子登录

2FA (2 Factor Authentication) 双因子登录是指在输入用户名和密码之外，还需要输入另外一种验证方式，以增加账户的安全性。

### 1.2 OTP

OTP (One-Time Password): 表示一次性密码。

### 1.3 HOTP

HOTP (HMAC-based One-Time Password): 表示基于 HMAC 算法加密的一次性密码。

HOTP 是事件同步，通过某一特定的事件次序及相同的种子值作为输入，通过 HASH 算法运算出一致的密码。

### 1.4 TOTP

TOTP (Time-based One-Time Password)，表示基于时间戳算法的一次性密码。

TOTP 是时间同步，基于客户端的动态口令和动态口令验证服务器的时间比对，一般每 60 秒产生一个新口令，要求客户端和服务器能够十分精确的保持正确的时钟，客户端和服务端基于时间计算的动态口令才能一致。

## 2 - 代码实现自动生成谷歌 2FA 验证密码

谷歌双因子验证基于的是 TOTP。因此根据 TOTP 的原理，获取 KEY 和当前时间后，就可以得到验证密码。

为了使用方便，还可以把得到的验证密码直接写入系统的剪贴板，这样就可以直接粘贴。

代码见：

[Maoxie/mintotp (github.com)](https://github.com/Maoxie/mintotp)
