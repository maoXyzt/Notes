# 创建自启动的 Windows Service 程序

借助 Windows Service Wrapper 小工具，将程序转换为 Windows 服务，在服务中心配置自启动，从而在开机时 windows 自行启动 Nginx 服务。

## 1. 自启动工具下载

工具下载:

> [https://github.com/winsw/winsw](https://github.com/winsw/winsw)

## 2. 自启动工具安装

- 步骤一：下载后将该工具放入 Nginx 的安装目录下，并且将其重命名为 nginx-service.exe ；

- 步骤二：在 nginx 安装目录下新建服务日志文件夹 server-logs 文件夹, 用来存放 nginx 服务相关日志。

- 步骤三：在该目录下新建 nginx-service.xml 文件，写入配置信息，配置好了之后就可以通过这个将 Nginx 注册为 Windows 服务了。

文件配置内容如下：重点包括三个，日志文件位置、启动命令、关闭命令；我 nginx 目录为：D:\work\nginx\nginx-1.18.0，同学们根据自己的目录作相应修改。

```xml
<!-- nginx-service.xml -->
<service>
    <id>nginx</id>
    <name>nginx</name>
    <description>nginx</description>
    <logpath>D:\work\nginx\nginx-1.18.0\server-logs\</logpath>
    <logmode>roll</logmode>
    <depend></depend>
    <executable>D:\work\nginx\nginx-1.18.0\nginx.exe</executable>
    <stopexecutable>D:\work\nginx\nginx-1.18.0\nginx.exe -s stop</stopexecutable>
</service>
```

## 3. 把 nginx 加入到 windows 服务中

以上内容配置好了之后，在 nginx 安装目录下以管理员运行命令：.\nginx-service.exe install 就成功将其注册为 Windows 服务了。

win + R 运行 services.msc 可以在服务中看到 nginx 服务。

后续将启动方式改成自动即可；然后启动服务。
