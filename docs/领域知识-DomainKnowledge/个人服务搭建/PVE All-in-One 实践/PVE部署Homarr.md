---
NoteStatus: draft
---

# PVE 部署 Homarr

PVE 版本: 8.3.0

## 1 - 项目介绍

Homarr 的核心功能是作为一个美观且实用的起始页或导航中心，帮助用户集中管理和快速访问其内部网络中的各种自托管服务。

Homarr 的目标用户是那些运行了多个自托管服务的技术爱好者、极客和普通家庭用户。它的定位非常明确：

- **个人服务器/NAS 的“主屏幕”**：就像手机的桌面一样，Homarr 是您访问所有内网服务的起点。
- **简化操作，提升体验**：它解决了多个自托管应用入口分散、UI 风格各异的问题，提供了一个统一、美观、高效的交互界面。
- **低门槛的自动化与可视化**：即使是“小白”用户，也能通过简单的拖拽完成复杂的布局定制，无需深厚的编程知识。

项目主页: [Homarr documentation](https://homarr.dev/)

## 2 - 部署

Homarr 提供了多种部署方式 ([Getting started | Homarr documentation](https://homarr.dev/docs/category/installation-1))。

本文主要关注在 Proxmox Virtual Environment (PVE) 上的部署。

> 参考文档: <https://homarr.dev/docs/getting-started/installation/proxmox>

### 2.1 脚本

[Proxmox Community-Scripts](https://community-scripts.github.io/ProxmoxVE/) 提供了社区维护的安装脚本。

准备一个 linux container，用于安装 Homarr。

在 linux container 的 console 中执行以下命令:

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/ct/homarr.sh)"
```
