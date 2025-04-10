# PostgreSQL 数据库文件路径迁移

迁移方法有两种：

（1）重新初始化 postgresql 数据库，初始化时指定新的数据路径---`PGDATA`，然后在新的环境下将原有的数据库备份恢复一下。不过这个方法有点麻烦

（2）直接将现有的数据库文件全部拷贝到新的数据库路径下，然后重起数据库服务

第二种方法比较简单，因此，就详细描述一下第二种方法：

1、postgresql 安装后，默认的数据库路径是 `/var/lib/pgsql/9.x/data` ("9.x" 是版本号)

2、新建一个路径作为新的数据库数据路径，假如是 `/home/data`

```bash
sudo mkdir /home/data
sudo chown -R postgres:postgres data
sudo chmod 700 data
```

最后这个赋权命令是必须的，不然数据库启动会有问题的

3、文件拷贝，

首先要停止 postgresql 服务，然后拷贝文件到目标目录

```bash
sudo systemctl stop postgresql
sudo su - postgres
cp -rf /var/lib/pgsql/9.x/data/* /home/data
```

4、修改 service 文件

找到文件，

```bash
vim /usr/lib/systemd/system/postgresql*.service
```

修改这个文件中的 (在 `[Service]` 部分)：

```ini
Environment=PGDATA=/var/lib/pgsql/9.4/data/
```

将其修改为自己的新的数据路径：

```ini
Environment=PGDATA=/home/data/
```

至此所有的修改工作就完成了，这个方法比较简单，但是前提是 postgresql 已经作为服务添加到了 systemctl，这一点需要注意

5、此时可以重新启动 postgresql 了，但是，尝试了几个方法都不能成功，只有重启一下系统，才可以

reboot 系统

然后启动 postgres 服务

```bash
sudo systemctl restart posrgresql
```

所有的一切和原来一样一样地！顺利完成数据迁移。

为了避免数据迁移的工作，今后再新部署 postgresql 时，应该考虑到系统分区的问题，要避免使用默认的数据路径
