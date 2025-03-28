# Home Assistant 系统备份到 NAS

## 1 - 在 NAS 上准备存储路径

1. 在 nas 上开启 smb 服务
2. 创建一个共享文件夹，用于存放备份文件，假设文件夹为 `Backup`

## 2 - 在 Home Assistant 添加网络存储

设置 -> 系统 -> 存储 -> 添加网络存储

填写如下内容:

- 名称: 填写一个名字，比如 `ugnas`
- 用量: 选择 `备份`
- 服务器: 填写 nas 的 ip 地址（或者如果有域名，也可以填写域名，不带 "http://"）
- 协议: 选择 `Samba (CIFS)`
- 远程共享: 填写共享文件夹（之前创建的 `Backup` 文件夹）
- 用户名: nas 的用户名
- 密码: nas 的密码

填写后点击 “连接”。

## 3 - 开启自动备份

设置 -> 系统 -> 备份 -> 配置备份设置

首先，在“自动备份”下，设置自动备份的频率、时间等。

然后在“位置”下，选择启用刚才添加的网络存储。

在“加密密钥”下，记录加密密钥，以便在恢复备份时使用。

其余设置按需调整。
