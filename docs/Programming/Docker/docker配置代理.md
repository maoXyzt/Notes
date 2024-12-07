# docker 配置代理

> 注意：无论是docker run还是docker build，默认是网络隔绝的。 如果代理使用的是localhost:3128这类，则会无效。 这类仅限本地的代理，必须加上--network host才能正常使用。 而一般则需要配置代理的外部IP，而且代理本身要开启gateway模式。

> [Docker的三种网络代理配置](https://note.qidong.name/2020/05/docker-proxy/)

## pull

在执行docker pull时，是由守护进程dockerd来执行。因此，代理需要配在dockerd的环境中。而这个环境，则是受systemd所管控，因此实际是systemd的配置。

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo touch /etc/systemd/system/docker.service.d/proxy.conf
```

```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

## build

```bash
docker build . \
    --build-arg "HTTP_PROXY=http://proxy.example.com:8080/" \
    --build-arg "HTTPS_PROXY=http://proxy.example.com:8080/" \
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com" \
    -t your/image:tag

docker-compose build \
    --build-arg http_proxy=http://proxy.example.com \
    --build-arg https_proxy=http://proxy.example.com \
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com"
```