# nginx 配置常见问题

## 1. location 匹配规则

> [一文弄懂Nginx的location匹配](https://segmentfault.com/a/1190000013267839)

语法规则

```nginx
location [ = | ~ | ~* | ^~ ] uri { ... }
location @name { ... }
```

### 1.1 修饰符

- `=` 表示精确匹配。只有请求的url路径与后面的字符串完全相等时，才会命中。
- `~` 表示该规则是使用正则定义的，区分大小写。
- `~*` 表示该规则是使用正则定义的，不区分大小写。
- `^~` 表示如果该符号后面的字符是最佳匹配，采用该规则，不再进行后续的查找。

location的配置有两种形式，前缀字符和正则。

查找匹配的时候，先查找前缀字符，选择最长匹配项，再查找正则（如果匹配了`^~`修饰的前缀字符，则不再查找正则）。如果有正则匹配项，正则的优先级高于前缀字符。

正则的查找是按照在配置文件中的顺序进行的。因此正则的顺序很重要，建议越精细的放的越靠前。

使用`=`精准匹配可以加快查找的顺序，如果根域名经常被访问的话建议使用`=`。

### 1.2 location @name 的用法

`@` 用来定义一个命名location。主要用于内部重定向，不能用来处理正常的请求。其用法如下：

```nginx
location / {
    try_files $uri $uri/ @custom
}
location @custom {
    # ...do something
}
```

上例中，当尝试访问url找不到对应的文件就重定向到我们自定义的命名location（此处为custom）。

命名location中不能再嵌套其它的命名location。

### 1.3 URL尾部的`/`需不需要

第一点与location配置有关，其他两点无关。

**location中的字符有没有`/`都没有影响。**

- 也就是说`/user/`和`/user`是一样的。

**如果URL结构是`https://domain.com/`的形式，尾部有没有`/`都不会造成重定向。**

- 因为浏览器在发起请求的时候，默认加上了`/`。
- (虽然很多浏览器在地址栏里也不会显示`/`。这一点，可以访问baidu验证一下。)

**如果URL的结构是`https://domain.com/some-dir/`。尾部如果缺少`/`将导致重定向。**

- 根据约定，URL尾部的`/`表示目录，没有`/`表示文件。
- 访问`/some-dir/`时，服务器会自动去该目录下找对应的默认文件。如果访问`/some-dir`的话，服务器会先去找 some-dir 文件，找不到的话会将 some-dir 当成目录，重定向到`/some-dir/`，去该目录下找默认文件。

## 2. proxy_pass 代理转发

> [nginx 之 proxy_pass 接口转发的规则](https://segmentfault.com/a/1190000018933857)

### 2.1 proxy_pass 不含 path 时

只有 '/' 结尾，也是含有 path 的情况

- `http://host` - √
- `https://host` - √
- `http://host:port` - √
- `https://host:port` - √
- `http://host/` - x
- `http://host:port/` - x

这种情况下，会把匹配到的所有 path 直接穿透转发。

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:3000;
}
# http://127.0.0.1:80/api/cc
#   -> http://127.0.0.1:3000/api/cc
```

### 2.2 proxy_pass 含 path 时

这种情况下，url 里面会去掉 location 匹配的字符串，拼接到 proxy_pass 再进行转发。

注意，含 path 的情况，location 不能使用正则表达式。

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:3000/;
}
# http://127.0.0.1:80/api/cc
#   -> http://127.0.0.1:3000/cc
```

### 3. proxy_redirect 修改被代理服务器的重定向url

在使用 nginx 做反向代理功能时，有时会出现重定向的url不是我们想要的url:

> 请求 `http://localhost:8080/api/get_data`, 代理到 `http://localhost:8081/api/get_data`。
> 返回的数据中有重定向url `http://localhost:8081/api/redirect`。
> 我们希望重定向到 `http://localhost:8080/api/redirect`。

当上游服务器返回的响应是重定向或刷新请求（如HTTP响应码是301或者302）时，proxy_redirect可以重设HTTP headers 的`location`或`refresh`字段。

可用于 `http`、`server`、`location` 配置 block 中。

```nginx
# 语法
proxy_redirect [ default|off|redirect replacement ];
# 默认值
proxy_redirect default;
# redirect 是匹配的url，replacement 是替换的url。
# redirect 和 replacement 可以是字符串或者正则表达式。
# replacement 可以省略 http://host:port 部分，省略的话会使用 proxy_pass 中的值。
# replacement 可以使用变量。
```

default 表示将上游服务器返回的重定向url中的域名和端口替换为代理服务器的域名和端口。

```nginx
# 如下规则等效：
location /one/ {
    proxy_pass       http://upstream:port/kevin/;
    proxy_redirect   default;
}
location /one/ {
    proxy_pass       http://upstream:port/kevin/;
    proxy_redirect   http://upstream:port/kevin/   /one/;
}
```
