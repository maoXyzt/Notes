# Rime 输入法配置语言模型: 万象拼音模型

对于长句子输入，Rime 输入法的默认语言模型效果不佳。

可以考虑配置使用 [万象拼音模型](https://github.com/amzxyz/RIME-LMDG)。

## 1 - 安装万象拼音模型

首先在 [Release](https://github.com/amzxyz/RIME-LMDG/releases) 页面下载最新的模型文件。

(2025.03.31) 我选择了长期支持版本：模型文件为 `wanxiang-lts-zh-hans.gram`。

之后，移动配置文件到 Rime 的配置目录内:

* MacOS: `$HOME/Library/Rime/`
* Windows: `%APPDATA%\Rime\`

## 2 - 启用

在想要使用的输入法配置文件 (`*.custom.yaml`) 中进行配置。

例如，在 `double_pinyin_flypy.custom.yaml` 添加以下内容，`language: wanxiang-lts-zh-hans` 换成你下载的模型文件名:

> 依赖 [octagram](https://github.com/lotem/rime-octagram-data/?tab=readme-ov-file#%E5%85%AB%E8%82%A1%E6%96%87%E8%AA%9E%E6%B3%95)，默认已经安装

```yaml
__include: octagram   #启用语法模型
octagram:
  __patch:
    # 语言模型
    grammar:
      language: wanxiang-lts-zh-hans
      collocation_max_length: 5
      collocation_min_length: 2
    # translator 内加载
    translator/contextual_suggestions: true
    translator/max_homophones: 7
    translator/max_homographs: 7
```

配置完成后，重新部署Rime输入法。
