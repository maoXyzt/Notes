# 安装 chromedriver

## 1. 安装最新 google chrome

> [Google Chrome 网络浏览器](https://www.google.com/chrome/)

```bash
# Debian/Ubuntu
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# Fedora/openSUSE
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
```

接下来安装

```bash
# Debian/Ubuntu
sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
```

如果出现报错 `Package xxxxx is not installed.`

执行

```bash
sudo apt-get install -f
```

然后再重新执行安装命令。

## 2. 安装 xvfb

这个是为了让 chrome 可以无界面运行。命令：

```bash
sudo apt-get install xvfb
```

## 3. 安装 chromedriver

获取 chromedriver 的最新版本信息

```bash
LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
```

然后再进行下载：

```bash
wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
```

之后解压，赋予它执行权限

```bash
unzip chromedriver_linux64.zip && cd chromedriver_linux64
chmod +x chromedriver
```

再把它以动到 usr/bin 目录下

```bash
sudo mv chromedriver /usr/bin/
```
