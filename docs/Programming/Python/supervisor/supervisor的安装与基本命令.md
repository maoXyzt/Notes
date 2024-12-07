# supervisor 的安装与基本命令

## 1. 安装

```bash
sudo apt install supervisor

# 为了让非root权限用户也能执行 supervisord/supervisorctl 等命令，需要修改以下路径权限
sudo chmod 777 /var/run				# supervisor.sock 文件路径
sudo chmod 777 /etc/supervisor		# 配置文件路径
sudo chmod 777 /var/log/supervisor	# 日志路径
```

启动`supervisor`服务：
```bash
# -c: 指定配置文件路径
supervisor -c /etc/supervisor/supervisor.conf
```

启动后在`/var/run`路径下生成`supervisor.sock`

配置demo

```ini
[program:simple-task-server]
directory = /home/mocap/repos/simple-task-server   ; 程序启动时的工作目录
command = /home/mocap/miniconda3/envs/simple-task-server/bin/gunicorn -c deploy/gunicorn_conf.py manage:app   ; 启动命令
autostart = true     ; 在 supervisord 启动的时候也自动启动
startsecs = 5        ; 启动 5 秒后没有异常退出，就当作已经正常启动了
autorestart = true   ; 程序异常退出后自动重启
startretries = 3     ; 启动失败自动重试次数，默认是 3
user = mocap          ; 用哪个用户启动
redirect_stderr = true  ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /home/mocap/repos/simple-task-server/logs/supervisord_stdout.log
```

### 常见错误

1. 

```
unix:///var/run/supervisord.sock refused connection?
```

说明 supervisord 未启动

2. 

```
unix:///var/run/supervisor.sock no such file
```

创建`supervisor.sock`并赋予权限

```bash
sudo touch /var/run/supervisor.sock
sudo chmod 777 /var/run/supervisor.sock
sudo systemctl restart supervisor
```

## 2. 管理命令

用`systemctl`服务管理

```bash
sudo systemctl enable supervisor	# 开启服务
sudo systemctl disable supervisor

sudo systemctl start supervisor
sudo systemctl stop supervisor
sudo systemctl restart supervisor

sudo systemctl status supervisor	# 开启服务
```

`supervisorctl`命令

```bash
supervisorctl reload	# 重新加载配置文件。每次修改配置文件后需要执行此命令

supervisorctl start task-name
supervisorctl stop task-name
supervisorctl restart all	# all表示所有项目
```

