# 自动获取双因子登录验证码——OTP, HOTP, TOTP 基本原理

## 1. 谷歌双因子登录验证码原理

**OTP**：One-Time Password，表示一次性密码。

**HOTP**：HMAC-based One-Time Password，表示基于HMAC算法加密的一次性密码。

> TOTP 是时间同步，基于客户端的动态口令和动态口令验证服务器的时间比对，一般每60秒产生一个新口令，要求客户端和服务器能够十分精确的保持正确的时钟，客户端和服务端基于时间计算的动态口令才能一致。

**TOTP**：Time-based One-Time Password，表示基于时间戳算法的一次性密码。

> HOTP 是事件同步，通过某一特定的事件次序及相同的种子值作为输入，通过HASH算法运算出一致的密码。

谷歌双因子验证基于的是TOTP。因此根据TOTP的原理，获取KEY和当前时间后，就可以得到验证密码。

为了使用方便，还可以把得到的验证密码直接写入系统的剪贴板，这样就可以直接粘贴。

## 2. 代码实现

[Maoxie/mintotp (github.com)](https://github.com/Maoxie/mintotp)
