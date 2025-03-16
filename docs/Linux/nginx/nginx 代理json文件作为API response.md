# nginx 代理json文件作为API response

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    root /var/www;
    location /api/endpoint {
        default_type application/json;
        index apiResponse.json;
        alias /var/www/;
    }
}
```
