---
type: note
aliases: []
created: 2026-05-07T18:00:51.000+0800
modified: 2026-05-07T19:28:38.416+0800
---

## 1 - 项目简介

> 原始 [asdlokj1qpi233/subconverter](https://github.com/asdlokj1qpi233/subconverter) 项目比较旧，不支持新的协议。
>
> 本文部署的是 [Aethersailor/SubConverter**-Extended](https://github.com/Aethersailor/SubConverter-Extended)
>
> Docker Image: [aethersailor/subconverter-extended](https://hub.docker.com/r/aethersailor/subconverter-extended)

subconvert: 略

subweb: 基于 subconverter 订阅转换的前端项目,方便用户快速生成各平台的订阅链接

## 2 - 使用 Docker Compose 部署 RustFS

### 2.1 项目配置

`docker-compose.yml`

```yaml
services:
  subconverter:
    image: aethersailor/subconverter-extended:latest
    container_name: subconverter
    ports:
      - "25500:25500"
    volumes:
	  - ./data/base/pref.toml:/base/pref.toml
    restart: unless-stopped
    environment:
      # 可选
      MANAGED_CONFIG_PREFIX: "http://<IP>:25500"
    environment:
      - TZ=Asia/Shanghai
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  subweb:
    image: careywang/subweb:latest
    container_name: subweb
    restart: unless-stopped
    ports:
      - "58080:80"
```

项目挂载路径:

- `./data/base/pref.toml:/base/pref.toml`: 配置路径

项目的端口映射:

- `25500:25500`: subconverter 服务端口
- `58080:80`: subweb 服务地址

环境变量:

- `MANAGED_CONFIG_PREFIX`: (可选) 非本机部署时，填上 IP 或者域名。等价于配置项: `[managed_config].managed_config_prefix`

## 3 - 使用

建议请求时带上 `config` 参数，使用 "Custom_OpenClash_Rules"

```bash
curl "http://<IP>:25500/sub?target=clash&url=YOUR_SUB&config=https://raw.githubusercontent.com/Aethersailor/Custom_OpenClash_Rules/main/cfg/Custom_Clash.ini"
```
