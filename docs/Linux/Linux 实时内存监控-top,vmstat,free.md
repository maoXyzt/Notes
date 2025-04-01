# Linux 实时内存监控: top, vmstat, free

## 1 - `top` 命令

实时监控系统运行状态，并且可以按照 cpu 及内存进行排序

```bash
-h: 帮助
-p: 监控指定的进程，当监控多个进程时，进程ID以逗号分隔，这个选项只能在命令行下使用
-M: 按内存使用率排序
-P: 按CPU使用率排序
-z: 彩色/黑白显示
```

load average: 系统的运行队列的平均使用率，也是可以认为是可运行进程的平均数，
三个值分别代表最后的 1 分钟，5 分钟，15 分钟的平均负载值。

在单核 cpu 中 load average 的值为 1 时表示满负荷状态，同理在多核 cpu 中满负载的 load average 的值为 1*cpu 的核数。

输入 top 后，按下 shfit+M 可以根据内存使用率排序.顺便瞅一眼 load average ，%cpu 这一列，id 前面的是空闲 cpu。

## 2 - `vmstat` 命令

可以监控操作系统进程状态，内存，虚拟内存，磁盘 IO，CPU 信息。

语法

```bash
vmstat [-a][-n][-S unit][delay[count]]
```

* `-S`：使用指定单位显示，参数有 `[k|K|m|M]`, 分别代表 1000、1024、1000000、1048567 bytes，默认单位为 `K`(1024 bytes)

## 3 - `free` 命令

能够监控系统内存的使用状态

```bash
free -h #（单位换算，更清晰）
```

* total: 总计物理内存的大小
* Used: 已使用多大
* Free: 可用有多少
* shared: 多个进程共享的内存总额
* buffers/cached: 磁盘缓存的大小
