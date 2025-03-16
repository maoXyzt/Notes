# convmv 解决GBK 迁移到 UTF-8, 中文文件名乱码

## 安装 convmv

```bash
yum install convmv
```

## 文件名编码转换命令

```bash
convmv -f GBK -t UTF-8 -r --nosmart --notest <目标目录>
```

* `-f`: from
* `-t`: to
* `--nosmart`: 如果已经是 utf－8 则忽略
* `-r`: 包含所有子目录
* `--notest`: 不加表示只列出有什么需要转换的，不做实际转换
