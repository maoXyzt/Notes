# 右键用 windows terminal 打开当前目录

参考 [右键菜单添加 "通过 xxx 打开"](./右键菜单添加“通过xxx打开”.md)，修改注册表。

通过搜索 `wt.exe` 定位分支位置。

修改 command 值，添加 `-d "%V"` 参数。
