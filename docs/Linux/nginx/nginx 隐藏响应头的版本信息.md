# nginx 隐藏响应 headers 中的版本信息

隐藏 headers 中的 server 字段

## 1. 将 nginx 版本号隐藏掉

修改 `nginx.conf` (`/etc/nginx/nginx.conf`) 配置文件，在配置文件中 http 类别下面增加如下配置：

```bash
server_tokens off;
```

然后重启

```bash
sudo nginx -s reload
```

## 2. 将 server 中的 nginx 替换为 `******`

需要更改 Nginx 的源码，然后重新编译安装，需要改动的源代码信息如下模块。
编辑 `src/http/ngx_http_header_filter_module.c` 文件，找到下面一行：

```c
static u_char ngx_http_server_string[] = "Server: nginx" CRLF;
```

将上面的 nginx 替换为 `******`

修改后，重新编译安装。
