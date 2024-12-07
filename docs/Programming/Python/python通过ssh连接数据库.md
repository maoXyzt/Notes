安装sshtunnel包，通过ssh到B机器，访问A机器上的数据库。

```python
import pymysql
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
  (sshServerB_ip, sshServerB_port), # B机器的配置
  ssh_password=sshServerB_pwd,
  ssh_username=sshServerB_usr,
  remote_bind_address=(databaseA_ip, databaseA_port)) as server: # A机器的配置

 db_connect = pymysql.connect(host='127.0.0.1', # 此处必须是是127.0.0.1
         port=server.local_bind_port,
         user=databaseA_usr,
         passwd=databaseA_pwd,
         db=databaseA_db)

 cur = db_connect.cursor()
 cur.execute('call storedProcedure')
 db_connect.commit()
```

