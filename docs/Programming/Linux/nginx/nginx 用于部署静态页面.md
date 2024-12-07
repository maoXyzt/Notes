# nginx 用于部署静态页面

Example:

```nginx
server {
    listen 8788;
    server_name 192.168.200.201;
    root /home/lzsjdev/internal_sys_test/linezonedata-internal-system-frontEnd/;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:8787;
    }
}
```
