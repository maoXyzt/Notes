# pip 命令换源

## 0. 临时使用

```bash
pip install -i https://pypi.douban.com/simple/ pandas
```

## 1. 直接配置

```bash
pip config set global.index-url https://pypi.douban.com/simple/
# # The output will be like:
# Writing to C:\Users\user123\AppData\Roaming\pip\pip.ini
```

使用命令也可以帮助找到pip配置文件的位置。

## 2. 修改配置文件

### 2.1 配置 pip 命令

**Linux：**

`$HOME/.config/pip/pip.conf`

或者

`$HOME/.pip/pip.conf`（推荐）

**Windows：**

`%HOME%\pip\pip.ini`

或者用`pip config set global.index-url https://pypi.douban.com/simple/`查看配置文件的位置

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

### 2.2 配置 setuptools / distutils 工具

使用 `setup.py` 安装依赖库, 即使配置了 pip 命令, 还是会从默认的 <http://pypi.python.org> 下载, 解决方案如下:

编辑 `~/.pydistutils.cfg` / `%APPDATA%\Python\pydistutils.cfg` 文件，内容如下:

```ini
[easy_install]
index_url = https://pypi.douban.com/simple
```

## 3. Q&A

Q: WARNING: The repository located at pypi.douban.com is not a trusted or secure host and is being ignored

A: pip不能使用 **http** 类型的连接，必须使用 **https** 的安全连接。将源路径改为 https
