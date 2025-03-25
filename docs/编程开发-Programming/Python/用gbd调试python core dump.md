# 用 gdb 调试 python core dump

## 1 - 安装 gdb

```bash
sudo apt install gdb
```

## 2 - 启动 gdb

```bash
gdb python
```

## 3 - 运行调试程序

```bash
run file.py
# 可以传各种参数
run -m scripts.test --path xxx/yy/z
```
