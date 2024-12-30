# 用gdb调试python core dump

## 0. 安装gdb

```bash
sudo apt install gdb
```

## 1. 启动gdb

```bash
gdb python
```

## 2. 运行调试程序

```bash
run file.py
# 可以传各种参数
run -m scripts.test --path xxx/yy/z
```
