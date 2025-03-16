# CentOS 7 lvm分区扩容

## 步骤

### 1. 新建一个物理分区

```bash
fdisk /dev/sda
n # 创建新分区，接下来按提示操作。新建主分区或逻辑分区都可以
```

假设新建的分区为 sda3 分区。
完成后重启。

### 2. 创建 sda3 分区建为物理卷

```bash
pvcreate /dev/sda3 # 路径可以参照 pvdisplay 这个命令中 sda1 的路径，一般都是在 dev 下
```

### 3. 为卷组 VolGroup00 添加新的物理卷 sda3 来增大卷组的容量

用 `vgdisplay` 来查看卷组名称

```bash
vgextend VolGroup00 /dev/sda3
```

### 4. 扩展逻辑卷的大小

用 `lvdisplay` 查看逻辑卷绝对路径

```bash
lvextend -L +2G /dev/VolGroup00/LogVol00
```

### 5.最后使用 resizefs2 命令重新加载逻辑卷

```bash
resize2fs /dev/VolGroup00/LogVol00
```

如果不用这个命令的话，你会发现用 `df -h` 命令查看扩展的逻辑卷大小还是原来的值，没有发生变化。即使重启也不会变，所以一定要执行 `resize2fs` 命令。
其中 `resize2fs` 加参数 `-f` 可以避免检查系统的时间消耗。
