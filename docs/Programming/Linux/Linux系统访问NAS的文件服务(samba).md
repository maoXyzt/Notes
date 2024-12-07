# Linux系统访问NAS的文件服务(samba)

适用于 samba 文件服务。

> 假设文件服务的IP地址为 `10.4.5.66`，帐号为`username_1`，密码为`password_1`。
>
> - 在 windows 系统下，直接在`win+r`或文件管理器地址栏输入 `\\10.4.5.66` 即可访问。
>
> - 在 mac 系统下，直接输入 `smb://10.4.5.66`。

## 安装 smbclient

```bash
sudo apt-get install smbclient
```

## 常用命令

### 1. 查看所有共享目录

```bash
smbclient -L 10.4.5.66 -U username_1
# Explicit password:
# smbclient -L 10.4.5.66 -U username_1%password_1
```

**当 SMB version 高于 SMB1 时，需要指定`-m smb3`（见Q1）**。

```
Domain=[ELSE_WORLDS] OS=[] Server=[]

        Sharename       Type      Comment
        ---------       ----      -------
        music           Disk      System default shared folder
        ReadOnly        Disk      
        share           Disk      
        web             Disk      System default shared folder
        IPC$            IPC       IPC Service ()
Domain=[ELSE_WORLDS] OS=[] Server=[]

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
```

### 2. 连接共享目录

```bash
smbclient //10.4.5.66/share -U username_1
# Explicit password:
# smbclient //10.4.5.66/share -U username_1%password_1
```

成功后出现提示符`smb:\>`，下面就可以开始操作。

**当 SMB version 高于 SMB1 时，需要指定`-m smb3`（见Q1）**。

### 3. 文件操作

| 命令                     | 说明                                                         |
| ------------------------ | ------------------------------------------------------------ |
| `?` or `help [command]`  | 提供关于帮助或某个命令的帮助                                 |
| `![shell command]`       | 执行所用的SHELL命令，或让用户进入 SHELL提示符                |
| `cd [目录]`              | 切换到服务器端的指定目录，如未指定，则 smbclient 返回当前本地目录 |
| `lcd [目录]`             | 切换到客户端指定的目录                                       |
| `dir` or `ls`            | 列出当前目录下的文件                                         |
| `exit` or `quit`         | 退出smbclient                                                |
| `get file1 [file2]`      | 从服务器上下载file1，并以文件名file2存在本地机上；如果不想改名，可以把file2省略 |
| `mget file1 file2 filen` | 从服务器上下载多个文件                                       |
| `md` or `mkdir [目录]`   | 在服务器上创建目录                                           |
| `rd` OR `rmdir [目录]`   | 删除服务器上的目录                                           |
| `put file1 [file2]`      | 向服务器上传一个文件file1，传到服务器上改名为file2           |
| `mput file1 file2 filen` | 向服务器上传多个文件                                         |

### 4. 临时挂载

```bash
sudo mount -t cifs -o username=username_1,password=password_1,file_mode=<filemode>,dir_mode=<dirmode>,gid=<ownerGroupID>,uid=<ownerID>,soft //10.4.5.27/share /home/yangzhitao/mnt/nas
```

**当 SMB version 高于 SMB1 时，需要指定vers（见Q2）**。

filemode, dirmode可指定挂载后的目录和文件权限（默认: 0755）。

gid/uid可指定挂载后的目录所属的组/用户（默认：当前用户(sudo时为root用户)和组）。

soft: soft mount. 默认为 hard mount，连接永不超时，无法中断。
> If the NFS file system is soft mounted, NFS tries repeatedly to contact the server until either:
> - A connection is established
> - The NFS retry threshold is met
> - The nfstimeout value is reached

### 5. 开机自动挂载

编辑 `/etc/fstab`

```bash
//10.4.5.66/share /path/of/mnt/point cifs user=username_1,password=password_1 0 0
```

## Q&A

Q1: `smbclient` 命令出现错误 `NT_STATUS_INVALID_NETWORK_RESPONSE`：

```bash
protocol negotiation failed: NT_STATUS_INVALID_NETWORK_RESPONSE
```

A1: 用`-m smb3` 指定 highest SME protocol level：

```bash
smbclient -m smb3 -L //10.4.5.66 -U username_1
```

The current Samba version in **Ubuntu 16.04** defaults to making NT1 (SMB1) connections even though it supports SMB2 and SMB3 - hence it works when you specify the client version from the command line. 

> [[solved\] [8.1.1] Samba access from Linux: protocol negotiation failed - General Support - LibreELEC Forum](https://forum.libreelec.tv/thread/9920-solved-8-1-1-samba-access-from-linux-protocol-negotiation-failed/)

Q2: `mount` 命令出现错误 `Operation not supported`：

```
mount: mount //10.4.5.66/share on /path/of/mnt/point failed: Operation not supported
```

A2: 需要指定 SMB 版本：

The SMB version needs to be specified when higher than v1

```bash
mount -t cifs \
  -o username=USERNAME,vers=3.0 \
  //10.4.5.66/share \
  /path/of/mnt/point
```

> [linux - Mounting cifs: "Operation not supported" - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/144522/mounting-cifs-operation-not-supported)

