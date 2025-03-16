# virtualbox 硬盘扩容

先把 VBoxManage 的路径配置在环境变量的 Path 中

然后到磁盘文件(.vdi 文件或.vmdk 文件)所在的位置打开命令窗口

```bash
# 磁盘格式为 vdi, 则可直接在 win 终端中执行如下命令：
VBoxManage modifyhd "centos7.vdi" --resize 51200    #（单位为 M）
# 输出内容如下
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
```

```bash
# 如果磁盘格式为 vmdk，则需要先转换为 vdi 格式，执行如下命令：
VBoxManage clonehd "centos7-disk001.vmdk" "centos7.vdi" --format vdi
VBoxManage modifyhd "centos7.vdi" --resize 51200    #（单位为 M）
# 可以在克隆的目录下查看文件是否克隆成功。
```
