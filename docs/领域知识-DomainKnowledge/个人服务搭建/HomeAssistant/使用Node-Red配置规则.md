# 使用 Node-RED 配置智能设备的自动化规则

Node-RED 是一个基于流的开发工具，它让你可以通过连接各种不同的节点来创建自动化任务和应用程序。

## １．　安装 Node-RED

### 1.1 安装 Node-RED

在 Home Assistant 界面中，进入 “设置” -> “加载项” -> “加载项商店”， 找到 Node-RED 并安装。

然后，点击 “启动” 按钮来启动 Node-RED 服务

### 1.2 安装 node-red-contrib-home-assistant-websocket

在 Home Assistant 界面中，进入 Node-RED 面板，点击右上角菜单按钮，选择 “节点管理”, 搜索并安装 "node-red-contrib-home-assistant-websocket"

### 1.3 安装 Node-RED Companion Integration

> <https://github.com/zachowj/hass-node-red>

1. 进入 HACS 面板
2. 搜索 "Node RED"，可以看到一个节点叫做 "Hass Node Red"，在右侧下拉菜单中点击 Download 进行下载
3. 在 "设置" -> "设备与服务" 中，点击 "添加集成" 按钮，搜索 "Node-RED"，点击 "Node-RED Companion" 进行安装

### 1.4 创建令牌

点击左下角用户名，在 “安全” 选项卡中，创建 “长期访问令牌”，并记录。

进入 Node-RED 面板，将任意一个 Home Assistant 节点拖入画布，双击节点。

在弹出的配置面板中，配置或新建 server，填入刚才创建的令牌到 Access token 输入框中，并勾选 “Accept Unauthorized SSL Certificates”。

(如果勾选了 “使用 Home Assistant 插件”，则不需要配置 Access token)

## 3. Node-RED 使用入门

> <https://sspai.com/post/88590>
> <https://blog.csdn.net/weixin_38767017/article/details/145602865>
> <https://www.xda-developers.com/how-i-use-node-red-and-home-assistant-together/>
