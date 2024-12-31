# 安装 FBX Python SDK

> - SDK 下载地址：
>
> [FBX Software Developer Kit 2020.0 | Autodesk Developer Network](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0?us_oa=dotcom-us&us_si=b6c98f47-851c-4638-88da-30cddc6a711f&us_st=fbx%20sdk)
>
> - 文档：
>
> [FBX SDK Help | Information and technical support | Autodesk](https://help.autodesk.com/view/FBX/2020/ENU/?guid=FBX_Developer_Help_welcome_to_the_fbx_sdk_technical_support_html)

文件说明：

- FBX SDK: C++版的 SDK。
- FBX Python SDK：python 版的 SDK，但只针对特定 python 版本(2.7)。
- FBX Python Bindings：用于编译指定版本的 FBX python SDK。

## 编译 FBX Python SDK

### 1. 安装编译依赖

#### 1.1 FBX SDK

下载 **FBX SDK**，解压后按照其中的文档（`Install_FbxSdk.txt`）说明进行安装。

Example:

```bash
# 安装到 `~/lib/FBX202001_FBXPYTHONBINDINGS_LINUX`
mkdir ~/lib/FBX202001_FBXPYTHONBINDINGS_LINUX
./fbx202001_fbxsdk_linux ~/FBX202001_FBXPYTHONBINDINGS_LINUX
```

之后把链接库路径添加到 `LD_LIBRARY_PATH` 中：

```bash
export LD_LIBRARY_PATH=~/lib/FBX202001_FBXFILESDK_LINUX/lib/gcc/x64/release/:$LD_LIBRARY_PATH
```

#### 1.2 libxml2 & libz

```bash
# ubuntu:
sudo apt install libxml2-dev
sudo apt install zlib1g zlib1g-dev
```

#### 1.3 sip 4.19.3

下载 sip 4.19.3 源代码并解压

> 源码：
>
> [PyQt - Browse /sip/sip-4.19.3 at SourceForge.net](https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.3/)

进入源码目录，编译安装

(1) 编译配置

```bash
python configure.py
```

(2) 如果在 ubuntu 系统上，修改 `sipconfig.py`，否则不能正确链接到 libxml2

> 原因：
>
> [FBX Python Bindings fails on Ubuntu because of undefined symbol xmlFree - Autodesk Community - FBX](https://forums.autodesk.com/t5/fbx-forum/fbx-python-bindings-fails-on-ubuntu-because-of-undefined-symbol/td-p/9538320)

修改 `sipconfig.py` 第 534 行：

```python
# before：
534         libs.extend(self.optional_list("LIBS"))
# after：
534         libs = list(self.optional_list("LIBS")) + libs
```

(3) 编译

```bash
make && make install
```

### 2. 编译

确定与当前 python 解释器匹配的选项（例如，`Python3_x64`）

```python
python PythonBindings.py
# Syntax: PythonBindings.py module module [buildsip] [test] [doc]
#

#         modules = Python2_x86 | Python2_ucs4_x86 | Python2_x64 | Python2_ucs4_x64 | Python3_x86 | Python3_x64 | Python2_ub | Python3_ub

# 对于 python2, 如果执行 python -c "import sys; print(sys.maxunicode)" 得到 1114111，则为 ucs4，否则为 ucs2
```

编译

```bash
python PythonBindings.py Python3_x64
```

找到编译产物

```bash
cd build/Distrib/site-packages/fbx
ls
# FbxCommon.py  fbx.so
```

复制文件到 `site-packages` 或 import 前把该路径添加到 `sys.path`。

测试

```python
import FbxCommon
(lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()
```
