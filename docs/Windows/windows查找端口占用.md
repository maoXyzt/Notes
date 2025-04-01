# windows 查找端口占用

## 查找端口占用

```bash
netstat -ano | findstr "8080"
```

## 查找进程 id 对应的进程

```bash
tasklist | findstr "8080"
```

## 关闭进程

```bash
taskkill /f /pid 1234
```

或者通过任务管理器，切换到“进程选项卡”，在 PID 一列中找到对应的进程。
