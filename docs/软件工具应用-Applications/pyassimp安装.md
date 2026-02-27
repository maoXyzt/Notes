---
NoteStatus: Draft
---

# PyAssimp 安装

## assimp 编译安装

### 下载源码

release v5.2.4 版本

### 编译环境

- gcc-9
- cmake

### 编译

创建 build 目录进行编译，方便重试时清理 cmake 产生的文件

```bash
mkdir build && cd build
cmake -D CMAKE_INSTALL_PREFIX=/usr \
    -D ASSIMP_BUILD_ZLIB=ON \
    ../CMakeList.txt
cmake --build .
cmake --install .
```

编译产物在 `CMAKE_INSTALL_PREFIX` 指定路径中

检查安装：

```bash
assimp version
```

## PyAssimp 安装

```bash
pip install pyasimp
```

为了适配 python3，需要做一些修改

链接库位置：

在 `port/PyAssimp/pyassimp/helper.py` 中定义

patchelf
