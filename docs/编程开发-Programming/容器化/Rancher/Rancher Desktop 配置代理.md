---
type: note
aliases: []
created: 2026-05-22T09:46:09.000+0800
modified: 2026-05-22T09:49:04.401+0800
---

在使用 Rancher Desktop 时，执行 `docker pull` 和 `docker compose pull` 的镜像拉取动作实际上是由 **Rancher Desktop 虚拟机内部的 Docker 守护进程（dockerd/Moby）** 执行的，而非宿主机直接发送请求。因此，为其配置代理的核心在于**为 Rancher Desktop 运行的虚拟机（WSL2 或 Lima）配置代理环境变量**。

以下是针对 **Windows** 和 **macOS** 系统最常用且有效的配置方法。

---

## 一、特别注意：本地代理软件的设置

如果你在宿主机上使用代理软件（如 Clash、v2ray 等），其默认监听的 `127.0.0.1` 仅限宿主机本地访问。虚拟机无法通过 `127.0.0.1` 访问到它。

1. **允许局域网连接**：在你的代理软件设置中，必须开启 **“允许局域网连接”（Allow LAN）**。
2. **代理端口**：确认你的代理软件 HTTP/Socks5 端口（例如 `7890`）。

---

## 二、Windows 系统配置方法（基于 WSL2）

在 Windows 上，Rancher Desktop 提供了原生的 WSL 代理配置界面，设置非常简单。

1. 打开 Rancher Desktop 主界面。
2. 点击右上角的 **Preferences（首选项齿轮图标）**。
3. 进入 **WSL** -> **Proxy** 选项卡。
4. 勾选 **Enable experimental proxy support**（启用代理支持）。
5. 在 **Proxy address** 中输入你的代理地址：
  - 格式通常为：`http://127.0.0.1:7890`（在 WSL 代理模式下，Rancher Desktop 会自动处理宿主机与虚拟机的网络映射关系，可以直接填 `127.0.0.1`）。
6. 如果代理需要账号密码，填写 **Authentication information**。
7. 在 **No proxy** 列表中填入不需要代理的地址（如 `localhost, 127.0.0.1, 0.0.0.0/8, 10.0.0.0/8` 等），避免内网流量被代理。
8. 点击 **Apply**（应用），Rancher Desktop 会自动重启相关服务，配置立即生效。

---

## 三、macOS 系统配置方法（基于 Lima 虚拟机）

macOS 版本没有直接的 GUI 代理配置页，可以通过以下两种方式为底层的 Lima 虚拟机配置代理。

### 方法 A：修改虚拟机配置文件（最直接，推荐）

1. 打开 macOS 的终端。
2. 进入 Rancher Desktop 虚拟机内部：

  ```bash

  rdctl shell

  ```

1. 编辑虚拟机的 Docker 配置文件：

  ```bash

  sudo vi /etc/conf.d/docker

  ```

1. 在文件末尾添加以下代理环境变量。**注意：** 必须使用 `host.lima.internal` 代替 `127.0.0.1`，以便虚拟机能够穿透访问宿主机的代理端口。

  ```bash
   export HTTP_PROXY="http://host.lima.internal:7890"
   export HTTPS_PROXY="http://host.lima.internal:7890"
   export NO_PROXY="localhost,127.0.0.1,cattle-system.svc,.svc,.cluster.local"
   ```

  *(请将 `7890` 替换为你实际的代理端口)*
2. 保存并退出 `vi`（输入 `:wq` 并回车）。
3. 重启 Docker 服务使配置生效：

  ```bash
   sudo rc-service docker restart

   ```

  或者直接通过 Rancher Desktop 图标重启整个软件。

### 方法 B：使用 `override.yaml` 永久保存（防软件更新重置）

如果你担心 Rancher Desktop 更新或重置时方法 A 的配置被抹除，可以使用 Lima 的覆盖配置机制。

1. 在宿主机（macOS）终端中，创建或编辑 `override.yaml` 文件：

  ```bash

  vi ~/Library/Application\ Support/rancher-desktop/lima/_config/override.yaml

  ```

2. 写入以下内容：

  ```yaml

  env:
    HTTP_PROXY: "http://host.lima.internal:7890"
    HTTPS_PROXY: "http://host.lima.internal:7890"
    NO_PROXY: "localhost,127.0.0.1,.example.com,cattle-system.svc"

  ```

3. 为允许虚拟机读取并应用该环境变量，需要修改虚拟机的 `rc.conf`：

  ```bash

  rdctl shell

  ```

  在虚拟机内部执行：

  ```bash

  sudo sed -i 's/^#rc_env_allow=".*/rc_env_allow="*"/' /etc/rc.conf

  ```

4. 重启 Rancher Desktop 即可。

---

## 四、验证代理是否配置成功

配置完成后，你可以通过以下命令进行验证：

1. **查看宿主机环境下的 Docker 信息**：
  在宿主机终端执行：

  ```bash

  docker info | grep -i proxy

  ```

  如果输出中正确显示了你配置的 `Http Proxy` 和 `Https Proxy` 变量，说明配置已经成功传递给 Docker 守护进程。

2. **拉取测试**：

  ```bash
  docker pull alpine
  # 或者
  docker compose pull
  ```

  观察拉取过程是否能够快速建立连接并完成下载。
