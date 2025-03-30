# Aqara 设备通过 Matter 接入 HomeAssistant

## 1 - 安装 Matter 集成

“设置” -> “设备与服务” -> “添加集成” -> 搜索 “Matter” -> 安装

安装完成后，在界面中点击“添加条目” -> “使用官方 Matter Server Supervisor 加载项” -> “提交”

![添加条目](./.assets/matter安装完成后添加条目.png)

## 2 - 添加 Aqara 设备

“设置” -> “设备与服务” -> “添加集成” -> 选择 “添加 Matter 设备”

并依次点击 “是的。已在使用中” -> “其他控制器”，然后出现输入设置代码的界面。

![添加 Matter 设备-1](./.assets/matter添加设备.png)
![添加 Matter 设备-2](./.assets/matter添加设备2.png)

此时打开 Aqara 的 App, 在网关设备的设置页，找到通用设置中的“Matter 生态”，生成“Matter 配对码”。将其输入到 HomeAssistant 中，点击“提交”即可。

之后按照需求将设备添加到仪表盘即可。
