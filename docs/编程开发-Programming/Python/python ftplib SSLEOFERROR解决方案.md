# python ftplib SSLEOFERROR 解决方案

## 1 - 问题描述

使用 ftplib 库连接 FTP 服务器时，出现 SSLEOFERROR 错误。

## 2 - 问题原因

FTP 服务端配置上要求客户端复用 session，即控制 session 和数据传输 session 必须相同。

## 3 - 解决方案

python 3.6 即以上版本，可以通过以下代码解决（继承 `ftplib.FTP_TLS` 类，重载 `ntransfercmd` 方法）

```python
class ReusedSslSocket(SSLSocket):
    def unwrap(self):
        pass


class MyFTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session"""
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn,
                                            server_hostname=self.host,
                                            session=self.sock.session)  # reuses TLS session
            conn.__class__ = ReusedSslSocket  # we should not close reused ssl socket when file transfers finish
        return conn, size
```
