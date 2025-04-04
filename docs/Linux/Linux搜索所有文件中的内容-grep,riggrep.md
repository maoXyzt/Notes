# Linux 搜索所有文件中的内容: grep, riggrep

有时候需要查找某个目录下的所有文件和子目录中的文件是否含有某个字符串，尤其在定位某个文件、代码段的时候非常好用。

## 使用 `grep` 命令

```bash
grep -rn 'hello,world!' *
```

`*` : 表示当前目录所有文件，也可以是某个文件名

- `-r`: 递归查找
- `-n`: 显示行号
- `-R`: 查找所有文件包含子目录
- `-i`: 忽略大小写
- `-l`: 只列出匹配的文件名
- `-L`: 列出不匹配的文件名
- `-w`: 只匹配整个单词，而不是字符串的一部分（匹配 hello，不匹配 helloo）

具体用法可以 `grep --help` 查看

## 更快的选择 `riggrep`

如果系统中安装了 [riggrep](https://github.com/BurntSushi/ripgrep)

把上述命令替换成：

```bash
rg -r -n 'hello,world!' *
```
