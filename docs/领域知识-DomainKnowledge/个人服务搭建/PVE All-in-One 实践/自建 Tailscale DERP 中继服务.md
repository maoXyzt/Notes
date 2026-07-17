---
type: note
aliases:
  - 自建 DERP 中继服务
created: 2026-07-16T03:07:32.000+0800
modified: 2026-07-16T03:07:32.000+0800
---

# 自建 Tailscale DERP 中继服务

> 官方文档：[DERP servers](https://tailscale.com/docs/reference/derp-servers)、[derper README](https://github.com/tailscale/tailscale/blob/main/cmd/derper/README.md)

当两台 Tailscale 设备无法建立直连时，DERP 会中继已经由 WireGuard 加密的流量。这里将 DERP 部署在有公网 IP 的 ECS 上，并启用 `verify-clients`，只允许当前 tailnet 的节点使用。

## 网络和域名

1. 将 DERP 域名的 A 记录解析到 ECS 公网 IPv4。
2. 在 ECS 安全组放行：
   - `8443/TCP`：DERP HTTPS 流量。
   - `3478/UDP`：STUN 探测。
   - `80/TCP` 和 `443/TCP`：仅在使用 ACME 客户端申请证书时按需开放。
3. `8443` 必须直接映射到 `derper`，不要经过 Caddy、Nginx 等 HTTP 反向代理。DERP 会在 TLS 连接内切换为自定义双向协议，与普通 HTTP 反向代理不兼容。

## 创建认证密钥

先在 [Access controls](https://login.tailscale.com/admin/acls/file) 中声明 tag：

```json
"tagOwners": {
  "tag:derp": ["autogroup:admin"]
}
```

然后进入 [Settings → Keys](https://login.tailscale.com/admin/settings/keys)，生成带 `tag:derp` 的 auth key：

- `Ephemeral`：关闭。
- `Pre-approved`：启用设备审批时开启。
- `Reusable`：通常关闭；只有需要用同一个 key 重复注册时才开启。

Auth key 只用于 `tailscaled` 首次加入 tailnet。部署使用持久化 state，容器重启后不需要重新注册。

## 部署服务

创建独立的部署目录：

```bash
mkdir -p derp/{certs,data/derper,data/tailscaled}
cd derp
```

创建 `.env`：

```ini
# derper 与 tailscaled 必须使用同一个精确版本
TAILSCALE_VERSION=v1.98.8
DERP_SERVER=derp.example.com
DERP_TS_AUTHKEY=tskey-auth-xxxx
```

准备域名对应的完整证书链和私钥。以 Certbot 的 HTTP-01 验证为例，确认 `80/TCP` 未被其他程序占用后执行：

```bash
export DERP_SERVER=derp.example.com

sudo certbot certonly --standalone -d "${DERP_SERVER}"

sudo install -m 0644 "/etc/letsencrypt/live/${DERP_SERVER}/fullchain.pem" \
  "./certs/${DERP_SERVER}.crt"
sudo install -m 0600 "/etc/letsencrypt/live/${DERP_SERVER}/privkey.pem" \
  "./certs/${DERP_SERVER}.key"
```

如果证书由 Caddy 或其他工具签发，复制相应的完整证书链和私钥即可。目标文件名必须是 `${DERP_SERVER}.crt` 和 `${DERP_SERVER}.key`。

创建 `Dockerfile`：

```dockerfile
FROM golang:1.26-alpine AS build

ARG TAILSCALE_VERSION
ARG GOPROXY=https://goproxy.cn,direct
ENV GOPROXY=${GOPROXY}
ENV GOTOOLCHAIN=auto

RUN test -n "${TAILSCALE_VERSION}" && \
    CGO_ENABLED=0 go install "tailscale.com/cmd/derper@${TAILSCALE_VERSION}"

FROM alpine:3.20

RUN apk add --no-cache ca-certificates
COPY --from=build /go/bin/derper /usr/local/bin/derper
```

创建 `docker-compose.yml`：

```yaml
services:
  tailscaled:
    image: "tailscale/tailscale:${TAILSCALE_VERSION:?TAILSCALE_VERSION must be set}"
    hostname: derp-verify
    environment:
      TS_AUTHKEY: ${DERP_TS_AUTHKEY}
      TS_USERSPACE: "true"
      TS_STATE_DIR: /var/lib/tailscale
      TS_TAILSCALED_EXTRA_ARGS: --socket=/var/run/tailscale/tailscaled.sock
    volumes:
      - ./data/tailscaled:/var/lib/tailscale
      - derp-tssock:/var/run/tailscale
    restart: unless-stopped

  derp:
    build:
      context: .
      args:
        TAILSCALE_VERSION: ${TAILSCALE_VERSION:?TAILSCALE_VERSION must be set}
    environment:
      DERP_SERVER: ${DERP_SERVER}
    entrypoint: ["/bin/sh"]
    command:
      - -c
      - |
        set -eu
        until [ -S /var/run/tailscale/tailscaled.sock ]; do sleep 1; done
        exec derper \
          -hostname="$${DERP_SERVER}" \
          -a=:8443 \
          -http-port=-1 \
          -stun \
          -stun-port=3478 \
          -certmode=manual \
          -certdir=/certs \
          -c=/data/derper.conf \
          -verify-clients
    ports:
      - "8443:8443"
      - "3478:3478/udp"
    volumes:
      - ./certs:/certs:ro
      - ./data/derper:/data
      - derp-tssock:/var/run/tailscale
    depends_on:
      - tailscaled
    restart: unless-stopped

volumes:
  derp-tssock:
```

`derper` 和负责 `verify-clients` 的 `tailscaled` sidecar 共用 `TAILSCALE_VERSION`。官方要求两者来自同一 Git revision；不要分别使用 `latest`。

启动并查看日志：

```bash
docker compose up -d --build derp tailscaled
docker compose ps derp tailscaled
docker compose logs -f derp tailscaled
```

以后升级只修改 `TAILSCALE_VERSION`，然后重新执行 `docker compose up -d --build derp tailscaled`。

证书续期后，覆盖 `certs/` 中的 `.crt` 和 `.key`，再执行 `docker compose restart derp` 让 `derper` 重新读取证书。

## 配置 Tailnet Policy

在 [Access controls](https://login.tailscale.com/admin/acls/file) 的顶层加入：

```json
"derpMap": {
  "OmitDefaultRegions": false,
  "Regions": {
    "900": {
      "RegionID": 900,
      "RegionCode": "myderp",
      "RegionName": "My DERP",
      "Nodes": [
        {
          "Name": "1",
          "RegionID": 900,
          "HostName": "derp.example.com",
          "DERPPort": 8443,
          "STUNPort": 3478
        }
      ]
    }
  }
}
```

保留 `OmitDefaultRegions: false`，让官方 DERP 在自建节点故障时继续兜底。

## 验证

在 macOS 或其他客户端执行：

```bash
tailscale debug derp myderp
tailscale netcheck
tailscale status
tailscale ping <另一台设备的主机名或 Tailscale IP>
```

成功标准：

- `debug derp` 显示成功建立 DERP connection，并收到 IPv4 STUN response。
- `netcheck` 的 DERP latency 中出现 `myderp` 和延迟。
- 实际走中继时，`status` 或 `ping` 显示 `relay "myderp"` / `via DERP(myderp)`。

## 常见问题

- `not authorized (not found in local tailscaled)`：先确认 `derper` 与 sidecar 使用同一个 `TAILSCALE_VERSION`，然后重新构建；同时确认 `derp-verify` 节点在 Machines 页面在线。
- `could not connect to relay server with ID '900'`：依次检查 DNS、`8443/TCP`、TLS 证书链、容器日志和 Tailnet Policy。
- 没有 DERP latency：重点检查 `3478/UDP`，不要误开放成 TCP。
- `generate_204`/port 80 warning：检查 Web 服务和安全组的 `80/TCP`；DERP 连接与 STUN 已成功时，这条 captive portal 检查告警不代表 `8443` 不通。
- 仅 IPv6 检查失败：如果服务只配置了公网 IPv4，且 IPv4 DERP 和 STUN 均成功，不影响 IPv4 使用；不要在 DNS 或 DERP Map 中声明不可达的 IPv6。

如果 auth key 泄露，在 Keys 页面撤销即可；撤销 auth key 不会断开已经注册的 sidecar。只有删除持久化的 `data/derp/tailscaled/` state 或删除 Machines 中的节点后，才需要使用新 key 重新注册。

