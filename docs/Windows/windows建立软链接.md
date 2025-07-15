# windows 创建软链接

## 创建软链接

```bash
# 建立d:\develop链接目录，指向远程的目标服务器上的e盘的对应目录
mklink /d d:\develop \\138.20.1.141\e$\develop
```

用法说明

- `/d`: 建立目录的符号链接(symbolic link)
- `/j`: 建立目录的软链接(junction)
- `/h`: 建立文件的硬链接(hard link)

## symbolic link, junction, hard link 的区别

> ["directory junction" vs "directory symbolic link"?](https://superuser.com/questions/343074/directory-junction-vs-directory-symbolic-link)

- symbolic link 是符号链接，可以跨盘符，可以跨分区
- junction 是目录链接，只能在本盘符内使用
- hard link 是硬链接，只能在本盘符内使用
