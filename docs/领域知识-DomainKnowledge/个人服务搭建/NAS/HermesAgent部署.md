---
type: note
aliases: []
created: 2026-04-15T14:00:37.000+0800
modified: 2026-04-28T21:53:59.365+0800
---

> 官方文档: <https://
> hermes-agent.nousresearch.com/docs/user-guide/docker#docker-compose-example>

> 本文编写时, `"nousresearch/hermes-agent"` 的最新版本为 `9d39e424be33` (2026-04-16)

编写 `docker-compose.yaml`:

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    # ports:
    #   - "8642:8642"
    volumes:
      - ./.hermes:/opt/data
    networks:
      - hermes-net
    stdin_open: true
    tty: true
    environment:
      - PATH=/opt/hermes/.venv/bin:/usr/local/bin:/usr/bin:/bin
    #   - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    #   - OPENAI_API_KEY=${OPENAI_API_KEY}
    #   - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"

  dashboard:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-dashboard
    restart: unless-stopped
    command: dashboard --host 0.0.0.0
    ports:
      - "9119:9119"
    volumes:
      - ./.hermes:/opt/data
    environment:
      - GATEWAY_HEALTH_URL=http://hermes:8642
    networks:
      - hermes-net
    depends_on:
      - hermes
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"

networks:
  hermes-net:
    driver: bridge
```

## Setup

启动容器后，先进入容器的终端 (`/bin/bash`), 执行:

```bash
su hermes
# 建议先 pip install qrcode 以便显示二维码
hermes setup
```

开始一些配置。

第一步，先配置模型平台（Inference Provider），需要提供相应的 API Key

第二步，配置 agent 要连接的通讯软件平台（Messaging Platforms）

```plaintext
◆ Messaging Platforms
  Connect to messaging platforms to chat with Hermes from anywhere.
  Toggle with Space, confirm with Enter.

  [ ]  1. Telegram
  [ ]  2. Discord
  [ ]  3. Slack
  [ ]  4. Signal
  [ ]  5. Email
  [ ]  6. SMS (Twilio)
  [ ]  7. Matrix
  [ ]  8. Mattermost
  [ ]  9. WhatsApp
  [ ] 10. DingTalk
  [ ] 11. Feishu / Lark
  [ ] 12. WeCom (Enterprise WeChat)
  [ ] 13. WeCom Callback (Self-Built App)
  [ ] 14. Weixin (WeChat)
  [ ] 15. BlueBubbles (iMessage)
  [ ] 16. QQ Bot
  [ ] 17. Webhooks (GitHub, GitLab, etc.)
```

其中，连接到飞书后，有一个选项是 `Home chat ID (optional, for cron/notifications)`。该项建议直接回车跳过，等机器人上线后去飞书里对它发 `/set-home` 即可。

> 因为飞书的 Chat ID（通常以 oc_ 开头）手动获取比较麻烦。而 Hermes Agent 提供了一个非常人性化的快捷绑定指令。

配置完成后，询问 `Launch hermes chat now? [Y/n]: `, 输入 Y 回车可以在终端中进行 chat，输入 n 回车则直接退出。

## pairing approve

向 agent 发消息，可能会得到如下回复:

```plaintext
Hi~ I don't recognize you yet!

Here's your pairing code: `69HXXXXX`

Ask the bot owner to run: `hermes pairing approve feishu 69HXXXXX`
```

再次进入终端，执行该命令即可。
