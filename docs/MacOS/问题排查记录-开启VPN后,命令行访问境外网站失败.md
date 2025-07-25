---
NoteStatus: draft
---

# 问题排查记录: 工作用的 MacBook 开启 VPN 后，命令行访问一些境外网站失败

2025-07-04

## 问题描述

问题表现：

公司更换 VPN 软件后，如果公司的 VPN，用 `git` 命令跟远端在 github.com 的仓库交互失败，ssh 到大部分服务器都不成功。

## 问题排查

### 1. 检查 DNS 解析

用 `ssh` 开启 `-v` 参数，查看 debug 信息，发现发送如下消息后没有收到远端服务。

```bash
debug1: SSH2_MSG_KEXINIT sent
```

由于通过浏览器是可以正常访问的，因此不存在连接问题。

如果直接通过 IP 建立 ssh 连接的话，一切正常。

怀疑是 DNS 问题。

用 `nslookup` 查看 DNS 解析，发现解析是通过 `127.0.0.1` 的 DNS 服务器，结果的 IP 地址是异常的:

```bash
> nslookup github.com
Server:  127.0.0.1
Address: 127.0.0.1#53

Non-authoritative answer:
Name: github.com
Address: 30.100.0.7
```

如果指定 DNS 服务器为 `223.5.5.5` (阿里云公共 DNS)则解析结果正常:

```bash
> nslookup github.com 223.5.5.5
Server:  223.5.5.5
Address: 223.5.5.5#53

Non-authoritative answer:
Name: github.com
Address: 20.205.243.166
```

用 `dig` 查看 DNS 解析，进一步验证了 DNS 服务器和解析结果是错误的:

```bash
❯ dig github.com

; <<>> DiG 9.10.6 <<>> github.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 14354
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;github.com.   IN A

;; ANSWER SECTION:
github.com.  300 IN A 30.100.0.10

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Fri Jul 04 22:22:20 CST 2025
;; MSG SIZE  rcvd: 54
```

### 2. 检查 DNS 服务器设置

查看 `/etc/resolv.conf` 文件，发现如果没有开启 VPN，其内容是:

```bash
#

# macOS Notice
#

# This file is not consulted for DNS hostname resolution, address
# resolution, or the DNS query routing mechanism used by most
# processes on this system.
#

# To view the DNS configuration used by this system, use:
#   scutil --dns
#

# SEE ALSO
#   dns-sd(1), scutil(8)
#

# This file is automatically generated.
#

nameserver 223.5.5.5
nameserver 114.114.114.114
```

跟我的网关（路由器）设置一致。

开启 VPN 后，`/etc/resolv.conf` 文件内容变为:

```bash
#

# macOS Notice
#

# This file is not consulted for DNS hostname resolution, address
# resolution, or the DNS query routing mechanism used by most
# processes on this system.
#

# To view the DNS configuration used by this system, use:
#   scutil --dns
#

# SEE ALSO
#   dns-sd(1), scutil(8)
#

# This file is automatically generated.
#

nameserver 127.0.0.1
nameserver ::1
```

通过 `scutil --dns` 查看 DNS 服务器设置，发现也是 `127.0.0.1` 和 `::1`。

```bash
❯ scutil --dns

DNS configuration

resolver #1
  nameserver[0] : 127.0.0.1
  nameserver[1] : ::1
  port     : 53
  if_index : 25 (utun6)
  flags    : Supplemental, Request A records, Request AAAA records
  reach    : 0x00000000 (Not Reachable)
  order    : 102600

resolver #2
  nameserver[0] : 223.5.5.5
  nameserver[1] : 114.114.114.114
  if_index : 14 (en0)
  flags    : Request A records
  reach    : 0x00000002 (Reachable)
  order    : 200000

resolver #3
  domain   : local
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300000

resolver #4
  domain   : 254.169.in-addr.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300200

resolver #5
  domain   : 8.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300400

resolver #6
  domain   : 9.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300600

resolver #7
  domain   : a.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 300800

resolver #8
  domain   : b.e.f.ip6.arpa
  options  : mdns
  timeout  : 5
  flags    : Request A records
  reach    : 0x00000000 (Not Reachable)
  order    : 301000

DNS configuration (for scoped queries)

resolver #1
  nameserver[0] : 223.5.5.5
  nameserver[1] : 114.114.114.114
  if_index : 14 (en0)
  flags    : Scoped, Request A records
  reach    : 0x00000002 (Reachable)

resolver #2
  nameserver[0] : 127.0.0.1
  nameserver[1] : ::1
  port     : 53
  if_index : 25 (utun6)
  flags    : Scoped, Request A records, Request AAAA records
  reach    : 0x00000000 (Not Reachable)
```

可以看到，resolver#1 的优先级高于 resolver#2。VPN 隧道流量(utun6)走 resolver#1，因此解析结果是错误的。

仅在命令行情况下会出现这个问题 。

### 3. 检查 DNS 请求流量

通过 `tcpdump` 查看 DNS 请求流量，发现请求流量是正常的。

在终端运行抓包命令:

```bash
sudo tcpdump -i utun6 port 53
```

在另一个终端运行 `nslookup` 命令:

```bash
nslookup github.com
```

在抓包终端可以看到 DNS 请求流量:

```bash
❯ sudo tcpdump -i utun6 port 53
Password:
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on utun6, link-type NULL (BSD loopback), snapshot length 524288 bytes
23:13:08.150506 IP 10.202.33.154.51312 > 10.9.190.119.domain: 40204+ [1au] A? github.com. (39)
23:13:08.161423 IP 10.9.190.119.domain > 10.202.33.154.51312: 40204 1/0/1 A 20.205.243.166 (55)
```

可以看到此时是通过 `10.9.190.119` 的 DNS 服务器解析的，结果是正确的。
