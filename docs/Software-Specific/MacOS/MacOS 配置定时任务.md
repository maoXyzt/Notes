# MacOS 配置定时任务

在 MacOS 上可以使用 `crontab` 或者 `launchd` 配置定时任务。 其中 `crontab` 已不推荐使用。

## 1. 使用 `launchd` 配置定时任务

`launchd` 是 MacOS 系统的任务调度器，可以用来配置定时任务。

`launchctl` 根据 plist 文件的信息来启动任务。
plist 脚本一般存放在以下目录：

* `/Library/LaunchDaemons`: 只要系统启动了，哪怕用户不登陆系统也会被执行
* `/Library/LaunchAgents`: 当用户登陆系统后才会被执行

> 更多的plist存放目录：
>
> * `~/Library/LaunchAgents`: 由用户自己定义的任务项
> * `/Library/LaunchAgents`: 由管理员为用户定义的任务项
> * `/Library/LaunchDaemons`: 由管理员定义的守护进程任务项
> * `/System/Library/LaunchAgents`: 由 Mac OS X 为用户定义的任务项
> * `/System/Library/LaunchDaemons`: 由 Mac OS X 定义的守护进程任务项

### 1.1 创建 plist 文件

进入 `~/Library/LaunchAgents`，创建一个 plist 文件 com.demo.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <!-- Label: 全局唯一的标识 -->
  <key>Label</key>
  <string>com.demo.plist</string>
  <!-- ProgramArguments: 命令及其参数 -->
  <key>ProgramArguments</key>
  <array>
    <string>/Users/demo/run.sh</string>
  </array>
  <!-- StartCalendarInterval: 指定要运行的时间 -->
  <key>StartCalendarInterval</key>
  <dict>
        <key>Minute</key>
        <integer>00</integer>
        <key>Hour</key>
        <integer>22</integer>
  </dict>
<!-- StandardOutPath: 标准输出文件 -->
<key>StandardOutPath</key>
<string>/Users/demo/run.log</string>
<!-- StandardErrorPath: 标准错误输出文件，错误日志 -->
<key>StandardErrorPath</key>
<string>/Users/demo/run.err</string>
</dict>
</plist>
```

`launchctl` 通过配置文件指定执行周期和任务，`launchctl` 的最小时间间隔是 1s (crontab 为分钟)。

支持两种方式配置执行时间：

* "StartInterval": 指定脚本每间隔多长时间（单位：秒）执行一次；
* "StartCalendarInterval": 可以指定脚本在多少分钟、小时、天、星期几、月时间上执行，类似如crontab的中的设置，包含下面的 key:
  * `Minute <integer>`: The minute on which this job will be run.
  * `Hour <integer>`: The hour on which this job will be run.
  * `Day <integer>`: The day on which this job will be run.
  * `Weekday <integer>`: The weekday on which this job will be run (0 and 7 are Sunday).
  * `Month <integer>`: The month on which this job will be run.

### 1.2 常用命令

> [launchctl Man Page](https://ss64.com/mac/launchctl.html)

```shell
# 加载任务, -w 选项会将plist文件中无效的key覆盖掉，建议加上
$ launchctl load -w /full-path/to/com.demo.plist

# 卸载任务
$ launchctl unload -w /full-path/to/com.demo.plist

# 查看任务列表, 使用 grep '任务部分名字' 过滤
$ launchctl list | grep 'com.demo'

# Manually run a known (loaded) agent/daemon, even if it is not the right time (Note: this command uses the agent's label, rather than the filename):
launchctl start com.demo.plist

# Manually kill the process associated with a known agent/daemon, if it is running:
launchctl stop com.demo.plist
```
