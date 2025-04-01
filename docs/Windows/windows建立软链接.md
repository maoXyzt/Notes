# windows 创建软链接

Example：

```bash
# 建立d:\develop链接目录，指向远程的目标服务器上的e盘的对应目录
mklink /d d:\develop \\138.20.1.141\e$\develop
```

用法说明

- `/d`: 建立目录的符号链接(symbolic link)
- `/j`: 建立目录的软链接(junction)
- `/h`: 建立文件的硬链接(hard link)
