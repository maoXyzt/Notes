# blender 安装 python packages

为了执行某些带第三方依赖的脚本，需要给 blender 自带的 python 环境安装一些包。

blender 的 python 环境默认不含 pip，因此需要先安装并升级 pip，然后再安装包。

## 1 - 确定 python 解释器的路径

启动 blender 自带的 python 解释器

```bash
blender -b --python-console
```

然后执行以下命令

```python
import sys
print(sys.prefix)
```

`sys.prefix`：为 python 安装的路径

> A string giving the site-specific directory prefix where the platform independent Python files are installed;
> by default, this is the string `/usr/local`. This can be set at build time with the `--prefix` argument to the **configure** script.
>
> The main collection of Python library modules is installed in the directory `*prefix*/lib/python<X.Y>`
> while the platform independent header files (all except `pyconfig.h`) are stored in `*prefix*/include/python<X.Y>`,
> where `<X.Y>` is the version number of Python, for example `3.2`.

python 解释器位于 `sys.prefix` 下的 `/bin/python3.7m`（文件名依具体 python 版本而定）

## 2 - 安装 pip

安装 pip 有两种途径：

- 执行 python 标准库自带的 `ensurepip` 模块(Python >= 3.4)
- 执行 pip 官网提供的 `get-pip.py` 脚本

### 2.1 方法一：ensurepip

假设上面找到的 python 解释器的路径为 /home/user/blender/current/2.83/python/bin/python3.7m

执行以下命令安装并升级 pip

```bash
/home/user/blender/current/2.83/python/bin/python3.7m -m ensurepip
/home/user/blender/current/2.83/python/bin/python3.7m -m ensurepip --upgrade
```

然后安装所需的包

```bash
/home/user/blender/current/2.83/python/bin/python3.7m -m pip install package_name
```

### 2.2 方法二：get-pip.py

如果 blender 是通过 snap 安装的，使用 `ensurepip` 时可能会遇到 Read Only 问题

> Could not install packages due to an EnvironmentError: [Errno 30] Read-only file system: '/snap/blender/current/2.83/python/lib/python3.7/site-packages/pip'

这时可以用 `get-pip.py` 安装 pip。

假设上面找到的 python 解释器的路径为 `/snap/blender/current/2.83/python/bin/python3.7m`

获取 `get-pip.py` 脚本并执行：

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# 确定具体路径
/snap/blender/current/2.83/python/bin/python3.7m get-pip.py
```

这时 pip 及之后安装的包将位于 `~/.local/lib/python3.7/site-packages`

## 3 - 安装 packages

启动 python 解释器

```bash
blender -b --python-console
# 或者直接通过上面找到的 python 路径启动
```

然后执行以下命令

```python
import site
import subprocess
import sys
from pathlib import Path

sys.path.append(site.USER_SITE)

# python_exe 为之前获得的 python 解释器的具体路径
python_exe = Path(sys.prefix) / 'bin' / 'python3.7m'
assert python_exe.exists()

# 安装包
subprocess.call([python_exe, "-m", "pip", "install", "package_name"])
```

使用 pip 及第三方库前，必须加上：

```python
import site
import sys
sys.path.append(site.USER_SITE)
```

否则会找不到库安装的位置。
