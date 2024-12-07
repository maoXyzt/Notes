## `top`命令

实时监控系统运行状态，并且可以按照cpu 及内存进行排序

```bash
-h: 帮助
-p: 监控指定的进程，当监控多个进程时，进程ID以逗号分隔，这个选项只能在命令行下使用
-M: 按内存使用率排序
-P: 按CPU使用率排序
-z: 彩色/黑白显示
```

load average :系统的运行队列的平均使用率，也是可以认为是可运行进程的平均数，
三个值分别代表最后的1分钟，5分钟，15分钟的平均负载值。

在单核cpu中load average的值为1时表示满负荷状态，同理在多核cpu中满负载的load average的值为1*cpu的核数。

输入top后，按下shfit+M 可以根据内存使用率排序.顺便瞅一眼load average ，%cpu 这一列，id 前面的是空闲cpu。

## `vmstat`命令

可以监控操作系统进程状态，内存，虚拟内存，磁盘IO，CPU信息。

语法

```bash
vmstat [-a][-n][-S unit][delay[count]]

-S ：使用指定单位显示，参数有k,K，m,M,分别代表1000、1024、1000000、1048567 bytes，默认单位为K（1024 bytes）
```

## `free`命令

能够监控系统内存的使用状态

```bash
free -h	#（单位换算，更清晰）
```

total:  总计物理内存的大小

Used:  已使用多大

Free: 可用有多少

shared: 多个进程共享的内存总额

buffers/cached: 磁盘缓存的大小
