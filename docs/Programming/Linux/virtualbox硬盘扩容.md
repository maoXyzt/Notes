# virtualbox 硬盘扩容

先把VBoxManage的路径配置在环境变量的Path中

然后到磁盘文件(.vdi文件或.vmdk文件)所在的位置打开命令窗口

```bash
# 磁盘格式为vdi,则可直接在win终端中执行如下命令：
VBoxManage modifyhd "centos7.vdi" --resize 51200    #（单位为M）
# 输出内容如下
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
```

```bash
# 如果磁盘格式为vmdk，则需要先转换为vdi格式，执行如下命令：
VBoxManage clonehd "centos7-disk001.vmdk" "centos7.vdi" --format vdi
VBoxManage modifyhd "centos7.vdi" --resize 51200    #（单位为M）
# 可以在克隆的目录下查看文件是否克隆成功。
```
