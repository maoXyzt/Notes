---
created: 2026-11-20T20:18:44.000+0800
modified: 2026-11-20T20:33:25.139+0800
---

## Komga 漫画与电子书服务部署

Komga 可以把 NAS 上的 CBZ、CBR、PDF 和 EPUB 整理成书库，供电纸书取书或手机浏览器直接阅读。

> [官方简介](https://komga.org/docs/introduction/)

### 1 - 在 NAS 上部署

将下面的配置保存为 `docker-compose.yaml`

```

```yaml
services:
  komga:
    image: gotson/komga:latest
    container_name: komga
    # user: "1000:10"
    volumes:
      - ./config:/config
      - ./data:/data
    ports:
      - "25600:25600"
    environment:
      TZ: Asia/Shanghai
      SPRING_SESSION_TIMEOUT: "30d"
      KOMGA_OAUTH2ACCOUNTCREATION: "false"  # 禁用OAuth2登录时创建账户
    restart: unless-stopped
```

容器需要能写入 `config/` 以保存数据库、账号和阅读进度，并能读取 `data/` 下的书籍。配置使用上海时区，会话超时为 30 天，OAuth2 自动创建账号已关闭。

在项目目录运行以下命令。使用 NAS 的 Docker 项目界面时，也可以选择同一目录，导入 Compose 后启动。

```sh
docker compose config --quiet
docker compose up -d
docker compose ps
```

### 2 - 创建书库并验证

1. 在局域网浏览器打开 `http://<NAS-IP>:25600`，按首次设置提示填写邮箱和密码，创建管理员账号。
2. 在 NAS 的 `data/` 下按系列建立子目录，放入一本书，例如 `data/示例漫画/第01卷.cbz`。
3. 点击侧栏 **Libraries** 旁的 **+**，填写书库名称，浏览并选择容器内的 `/data`，保存后等待扫描。
4. 在网页打开刚加入的书并翻一页。若书库为空，先确认书籍实际位于挂载目录且容器可读；若网页打不开，在项目目录运行 `docker compose logs --tail=100 komga` 查看启动日志。[官方书库指南](https://komga.org/docs/guides/libraries/)

### 3 - 在电纸书取书，用手机续读

在电纸书的 KOReader 中添加 OPDS 书库，地址填 `http://<NAS-IP>:25600/opds/v1.2/catalog`，使用 Komga 账号登录。下载一本 EPUB 后即可离线阅读。手机在同一局域网中可以直接打开 Komga 网页。[官方 OPDS 指南](https://komga.org/docs/guides/opds/)

要在 KOReader 与手机网页之间同步位置，还需完成以下设置：

1. 在 Komga 为阅读账号授予 `KOREADER_SYNC` 权限，在相应书库启用 KOReader 文件哈希，等待文件分析完成。
2. 用该账号打开 **My Account**，生成并保存 API 密钥。
3. 在 KOReader 打开一本书，进入 **Progress sync → Custom sync server**，填写 `http://<NAS-IP>:25600/koreader`。
4. 在同步登录框的用户名栏填写 API 密钥，密码栏填任意占位值；文档匹配方式选择 **Binary**。使用从该书库下载的同一文件测试同步。

普通 EPUB 在 KOReader 与 Komga 之间切换时会定位到章节开头；固定分页书籍可以精确到页。[官方 KOReader 同步指南](https://komga.org/docs/guides/koreader/)

### 4 - 备份与恢复

在维护窗口停止 Komga，备份项目下的 `docker-compose.yaml`、`config/` 和 `data/`，完成后重新启动。恢复时将三者放回同一项目目录，保留挂载目录的权限，再执行 `docker compose up -d`。使用原账号登录，检查书库和阅读进度。
