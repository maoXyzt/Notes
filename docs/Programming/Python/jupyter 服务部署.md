# Jupyter 服务部署

> [Running a public Jupyter server — Jupyter Server documentation](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html)

## 0. 配置文件

配置文件 `jupyter_server_config.py` 位于以下位置：

- Windows: `%USERPROFILE%\.jupyter\jupyter_server_config.py`
- OS X: `~/.jupyter/jupyter_server_config.py`
- Linux: `~/.jupyter/jupyter_server_config.py`

如果没有配置文件，可执行以下命令生成：

```bash
jupyter server --generate-config
```

## 1. 配置服务密码

### 1.1 自动初始化密码

首次用token登录时，在UI界面上会拥有一次设置密码的机会。之后登录就会要求输入新密码，而非token。

也可以用命令设置密码。这一命令可以用来重置丢失的密码。

```bash
$ jupyter server password
Enter password:  ****
Verify password: ****
```

### 1.2 手动填写哈希密码

手动生成哈希过的密码

```python
from jupyter_server.auth import passwd
passwd()
# 输入密码
```

然后将生成的哈希后的密码填入 `jupyter_server_config.py`，如：

```python
c.ServerApp.password = u'sha1:67c9e60bb8b6:9ffede0825894254b2e042ea597d771089e11aed'
```

自动填写的密码会被储存在`jupyter_server_config.json`中，它的优先级比`jupyter_server_config.py`高，因此手动填写的密码可能不能生效。

## 2. 使用SSL连接

### 2.1 配置 SSL

修改 `jupyter_server_config.py` 中的如下选项:

```python
# Set options for certfile
c.ServerApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem'
c.ServerApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'
```

或者在启动时指定密钥文件

```bash
jupyter server --certfile=mycert.pem --keyfile mykey.key
```

### 2.2 获取证书

自签名证书可以用以下命令生成：

```bash
# 有效期为365天
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.pem
```

或者使用 [Let's Encrypt](https://letsencrypt.org/) 生成证书 [Using Let's Encrypt](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#using-lets-encrypt)。

## 3. 配置public notebook server

修改`jupyter_server_config.py`中的如下选项

```python
# Set options for certfile, ip, password, and toggle off
# browser auto-opening
c.ServerApp.certfile = u'/absolute/path/to/your/certificate/mycert.pem'
c.ServerApp.keyfile = u'/absolute/path/to/your/certificate/mykey.key'
# Set ip to '*' to bind on all interfaces (ips) for the public server
c.ServerApp.ip = '*'
c.ServerApp.password = u'sha1:bcd259ccf...<your hashed password here>'
c.ServerApp.open_browser = False

# It is a good idea to set a known, fixed port for server access
c.ServerApp.port = 9999
```

通过以下命令启动服务

```bash
jupyter server
```

## 4. 其他配置

### 4.1 配置 base url

默认 base url 为`/`，通过类似 `http://localhost:8888/` 的 URL 访问。

修改`jupyter_server_config.py`中的如下选项，实现通过 `http://localhost:8888/ipython/` 访问 Jupyter Server。

```python
c.ServerApp.base_url = "/ipython/"
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
