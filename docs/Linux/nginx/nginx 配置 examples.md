# nginx 配置 examples

## 1. 用于部署静态页面

文件在 `/var/www/html` 目录下，网页配置到 `/` 路径下。

```nginx
location / {
    root /var/www/html/;
    index index.html;
    try_files $uri $uri/ /index.html;
}
```

### 子目录

文件在 `/var/www/html` 目录下，网页配置到 `/html/` 路径下。

```nginx
location /html/ {
    root /var/www;
    index index.html;
    try_files $uri $uri/ /html/index.html;
}
```

文件在 `/var/www/html` 目录下，网页配置到 `/pages/` 路径下。

```nginx
location /pages/ {
    alias /var/www/html/;
    index index.html;
    try_files $uri $uri/ /index.html;
}
```

## 2. 代理 API 请求

代理 `/api/*` 路径下的所有请求，代理到 `http://localhost:3000/api/*`。

```nginx
location /api/ {
    proxy_pass http://localhost:3000;
}
```

代理 `/api/*` 路径下的所有请求，代理到 `http://localhost:3000/*`。

```nginx
location /api/ {
    proxy_pass http://localhost:3000/;

}
```

### 正则表达式匹配路径

使用正则表达式匹配路径，代理 `/api/*` 路径下的所有请求，代理到 `http://localhost:3000/api/*`。

```nginx
location ~ /api/ {
    proxy_pass http://localhost:3000;
}
```

### 代理 websocket 请求

```nginx
location /ws/ {
    proxy_pass http://localhost:3000/ws/;

    client_max_body_size 1024m;
    client_body_buffer_size 2048m;

    # Enable WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_buffering  off;
}
```
