# python通过ssh连接数据库

安装 `sshtunnel` 包，通过ssh到B机器，访问A机器上的数据库。

```python
import pymysql
from sshtunnel import SSHTunnelForwarder

# 配置B机器的 ssh 连接信息
sshServerB_ip = '192.168.1.1'
sshServerB_port = 22
sshServerB_usr = 'root'
sshServerB_pwd = '123456'
databaseA_ip = '192.168.1.2'
databaseA_port = 3306
databaseA_usr = 'root'
databaseA_pwd = '123456'
databaseA_db = 'test'

with SSHTunnelForwarder(
    (sshServerB_ip, sshServerB_port),  # B机器的配置
    ssh_username=sshServerB_usr,
    ssh_password=sshServerB_pwd,
    remote_bind_address=(databaseA_ip, databaseA_port),
) as server:  # A机器的配置
    db_connect = pymysql.connect(
        host='127.0.0.1',  # 此处必须是是127.0.0.1
        port=server.local_bind_port,
        user=databaseA_usr,
        passwd=databaseA_pwd,
        db=databaseA_db,
    )

    cur = db_connect.cursor()
    cur.execute('call storedProcedure')
    db_connect.commit()
```
