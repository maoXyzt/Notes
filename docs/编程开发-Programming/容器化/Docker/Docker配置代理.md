# Docker 配置代理

> 注意：无论是 `docker run` 还是 `docker build`，默认是网络隔绝的。
> 如果代理使用的是 "localhost:3128" 这类，则会无效。
> 这类仅限本地的代理，必须加上 `--network host` 才能正常使用。 而一般则需要配置代理的外部 IP，而且代理本身要开启 gateway 模式。
>
> [Docker 的三种网络代理配置](https://note.qidong.name/2020/05/docker-proxy/)

## pull & push

> 关联内容: [Docker 配置镜像源](./Docker%20配置镜像源(registry-mirrors).md)

在执行 `docker pull` 和 `docker push` 时，是由守护进程 dockerd 来执行。
因此，代理需要配在 dockerd 的环境中。而这个环境，则是受 systemd 所管控，因此实际是 systemd 的配置。

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo touch /etc/systemd/system/docker.service.d/proxy.conf
```

```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com,.cn"
```

## build

```bash
docker build . \
    --build-arg "HTTP_PROXY=http://proxy.example.com:8080/" \
    --build-arg "HTTPS_PROXY=http://proxy.example.com:8080/" \
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com,.cn" \
    -t your/image:tag

docker-compose build \
    --build-arg http_proxy=http://proxy.example.com \
    --build-arg https_proxy=http://proxy.example.com \
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com,.cn"
```
