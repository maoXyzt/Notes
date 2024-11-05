# Jupyter 服务部署

> [Running a notebook server — Jupyter Notebook 6.2.0 documentation (jupyter-notebook.readthedocs.io)](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html)

## 0. 配置文件

配置文件`jupyter_notebook_config.py`位于以下位置：

- Windows: `C:\Users\USERNAME\.jupyter\jupyter_notebook_config.py`
- OS X: `/Users/USERNAME/.jupyter/jupyter_notebook_config.py`
- Linux: `/home/USERNAME/.jupyter/jupyter_notebook_config.py`

如果没有配置文件，可执行以下命令生成：

```bash
jupyter notebook --generate-config
```

## 1. 自动初始化密码

首次用token登录时，在UI界面上会拥有一次设置密码的机会。之后登录就会要求输入新密码，而非token。

也可以用命令设置密码。这一命令可以用来重置丢失的密码。

```bash
$ jupyter notebook password
Enter password:  ****
Verify password: ****
```

## 2. 手动填写哈希密码

手动生成哈希过的密码

```python
from notebook.auth import passwd
passwd()
# 输入密码
```

然后将哈希后的密码填入`jupyter_notebook_config.py`，如：

```python
c.NotebookApp.password = u'sha1:67c9e60bb8b6:9ffede0825894254b2e042ea597d771089e11aed'
```

自动填写的密码会被储存在`jupyter_notebook_config.json`中，它的优先级比`jupyter_notebook_config.py`高，因此手动填写的密码可能不能生效。

## 3. 使用SSL连接

在启动时用以下选项指定密钥文件，开启SSL连接

```bash
jupyter notebook --certfile=mycert.pem --keyfile mykey.key
```

或者修改`jupyter_notebook_config.py`中的如下选项

```python
# Set options for certfile
c.NotebookApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem'
c.NotebookApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'
```

## 4. 配置public notebook server

修改`jupyter_notebook_config.py`中的如下选项

```python
# set ip, password, and toggle off browser auto-opening
# Set ip to '*' to bind on all interfaces (ips) for the public server
c.NotebookApp.ip = '*'
c.NotebookApp.password = u'sha1:bcd259ccf...<your hashed password here>'
c.NotebookApp.open_browser = False

# It is a good idea to set a known, fixed port for server access
c.NotebookApp.port = 9999
```

## 5. 管理 kernel

添加kernel：

> [Installing the IPython kernel — IPython 7.25.0 documentation](https://ipython.readthedocs.io/en/stable/install/kernel_install.html#kernels-for-different-environments)

```python
pip install ipykernel
python -m ipykernel install --user --name fbxpy38 --display-name "Python3.8 (fbx)"
```

删除kernel：

> [remove kernel on jupyter notebook - Stack Overflow](https://stackoverflow.com/questions/42635310/remove-kernel-on-jupyter-notebook)

```bash
jupyter kernelspec list
jupyter kernelspec uninstall unwanted-kernel
```
