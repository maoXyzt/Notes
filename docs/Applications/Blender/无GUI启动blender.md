## headless方式启动 blender

```bash
blender -b
```

 ## 启动blender的同时执行 python 脚本

```bash
blender -b -P my_script.py
```

### 给脚本传参

blender会把第一个`--`之后的参数传给脚本，但在脚本内部会获取到全部的参数而非只有`--`之后的参数，需要自己过滤掉它们。

```bash
blender -b -P my_script.py -- --number 5 --save '/Users/Jenny/Desktop/cube.obj'
```

## 打开python shell

```bash
blender -b --python-console
```

blender包含了一个python解释器，位于blender安装目录的`bin/<版本号>/python/bin/`路径内。

该python未包含pip，如果需要往这个python环境安装第三方依赖，可以先用如下命令安装pip：

```bash
<路径>/python -m ensurepip
```

## -noaudio 选项

启动时可能会出现以下报错

```bash
ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:4727:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM default
AL lib: (EE) ALCplaybackAlsa_open: Could not open playback device 'default': No such file or directory
found bundled python: /home/ubuntu/blender-2.74-linux-glibc211-x86_64/2.74/python

Blender quit
```

由于一般不需要声音，可以通过添加`-noaudio`选项来关掉这个错误。

```bash
blender -b -noaudio
```