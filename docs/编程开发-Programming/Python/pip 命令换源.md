# pip 命令换源 (含 PyTorch 源)

> 相关话题: [Conda 换源](./conda%20换源.md)

* 豆瓣源: <https://pypi.douban.com/simple/>
* 清华源: <https://pypi.tuna.tsinghua.edu.cn/simple>
* 阿里源: <https://mirrors.aliyun.com/pypi/simple/>

## 1 - 一次性临时使用

```bash
pip install -i https://pypi.douban.com/simple/ pandas
```

## 2 - 通过命令行配置

```bash
pip config set global.index-url https://pypi.douban.com/simple/
# # The output will be like:
# Writing to C:\Users\user123\AppData\Roaming\pip\pip.ini
```

使用命令也可以帮助找到 pip 配置文件的位置。

## 3 - 修改配置文件

### 3.1 配置 pip 命令

**Linux：**

`$HOME/.config/pip/pip.conf`

或者

`$HOME/.pip/pip.conf`（推荐）

**Windows：**

`%HOME%\pip\pip.ini`

或者用 `pip config set global.index-url https://pypi.douban.com/simple/` 查看配置文件的位置

配置文件内容：

```ini
[global]
index-url = https://pypi.douban.com/simple/
trusted-host = pypi.douban.com
[install]
use-mirrors = true
mirrors = https://pypi.douban.com/simple/
trusted-host = pypi.douban.com
```

也可以简写为：

```ini
[global]
index-url = https://pypi.douban.com/simple/
[install]
trusted-host = pypi.douban.com
```

### 3.2 配置 setuptools / distutils 工具

使用 `setup.py` 安装依赖库, 即使配置了 pip 命令, 还是会从默认的 <http://pypi.python.org> 下载, 解决方案如下:

编辑 `~/.pydistutils.cfg` / `%APPDATA%\Python\pydistutils.cfg` 文件，内容如下:

```ini
[easy_install]
index_url = https://pypi.douban.com/simple
```

## 4. 使用国内镜像加速安装 PyTorch

* 阿里Pytorch源: <https://mirrors.aliyun.com/pytorch-wheels/>
* 上海交通大学Pytorch源: <https://mirror.sjtu.edu.cn/pytorch-wheels/>

使用方法: 把官方的 PyTorch 源 (<https://download.pytorch.org/whl/cu118>) 替换为国内源

```bash
# 用阿里云的源
pip3 install torch==2.4.1 torchvision torchaudio -f https://mirrors.aliyun.com/pytorch-wheels/cu121
# 用上海交通大学的源
pip3 install torch==2.4.1 torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/cu121
# 或者
pip3 install torch==2.4.1 torchvision torchaudio -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
```

## 5. Q&A

Q1: WARNING: The repository located at pypi.douban.com is not a trusted or secure host and is being ignored

A1: pip 不能使用 **http** 类型的连接，必须使用 **https** 的安全连接。将源路径改为 https
