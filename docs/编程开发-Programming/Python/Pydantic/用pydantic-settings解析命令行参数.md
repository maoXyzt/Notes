# 用 Pydantic Settings 解析命令行参数

Pydantic Settings 除了可以从环境变量，.env 文件，.yaml/.json/.toml 文件获取配置值之外，

从 Pydantic 的 2.7 版本起，`BaseSettings` 类支持从命令行参数解析。本文编写时使用 2.11 版本。

## 0 - 为什么选择用 Pydantic Settings 解析命令行参数

- `argparse` 库对类型支持不友好，且验证能力弱
- `typer` 对类型友好，数据验证能力强，输出格式友好；但缺少配置文件解析功能，所有参数都要从命令行传入

稍复杂的应用经常会需要实现一个 Settings 类进行配置的初始化、校验，并在应用间传递配置函数。
`pydantic-settings` 支持从命令行解析参数，并支持类型验证，配置文件解析，环境变量解析。
实例化的对象可直接在函数间传递使用。不再需要先解析和校验命令行参数，再传给 settings 实例使用。减少重复编写校验逻辑。

## 1 - 使用方法

> <https://docs.pydantic.dev/2.11/concepts/pydantic_settings/#command-line-support>

### 1.1 - 定义 Settings 类

需要在model_config中设置 `cli_parse_args=True`

```python
# main.py
from typing import Annotated
from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        cli_parse_args=True,
        cli_ignore_unknown_args=True,
        cli_exit_on_error=True,
        cli_kebab_case=True,
        # 其他选项...
    )

    # 定义配置项，例如:
    system_message: str = Field(
        "You are a helpful assistant who can describe video content."
        " Do not include any text in the background."
        " Do not describe subtitles."
        " Do not include any other information.",
        description="System prompt",
    )
    prompt: str = Field(
        "Please describe whether cuts or transitions occur in the video."
        " Please only answer yes or no and do not include any other information.",
        description="Prompt",
    )
    api_key: Annotated[SecretStr, Field(alias="API_KEY")] = SecretStr("")
    ...
```

- `cli_parse_args=True` 表示从命令行解析参数
- `cli_ignore_unknown_args=True` 表示忽略未知参数
- `cli_exit_on_error=True` 表示在解析错误时退出
- `cli_kebab_case=True` 表示使用 kebab-case 格式。如 `my_option` 对应的命令行参数为 `--my-option`。

相关的 Field 选项:

- `description`: 参数用于描述参数的用途，在命令行中使用 `--help` 选项时会显示。
- `alias`: 参数用于设置配置项名称，也会影响命令行参数名称
  - 这里虽然 alias 为 UPPER_CASE，但命令行参数仍会被 `cli_kebab_case` 选项转换为 kebab-case 格式

### 1.2 - 使用 Settings 类

使用 `CliApp.run(Settings)` 解析命令行参数，并返回 Settings 实例。

之后将 Settings 实例作为参数传递给程序的入口函数使用。

```python
# main.py
from typing import Annotated
from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict

class Settings(BaseSettings):
    ...

def main(settings: Settings):
    ...

if __name__ == "__main__":
    settings = CliApp.run(Settings)
    main(settings)
```

在命令行中使用 `--help` 选项时会显示配置项的描述。

```bash
python main.py --help
```

```bash
usage: detect_video_cuts_by_gemini.py [-h] [--system-message str] [--prompt str] [--api-key SecretStr]

Settings for the detect video cuts by gemini.

options:
  -h, --help            show this help message and exit
  --system-message str  System prompt (default: You are a helpful assistant who can describe video content. Do not include any text in the background. Do not describe subtitles. Do not include any other information.)
  --prompt str          Prompt (default: Please describe whether cuts or transitions occur in the video. Please only answer yes or no and do not include any other information.)
  --api-key SecretStr   (default: )
```

### 1.3 - 命令行传参

命令行参数的格式为 `--key value` 或 `--key=value`

对于 list 类型，支持3种传参格式:

- JSON style: `--field='[1,2]'`
- Argparse style: `--field 1 --field 2`
- Lazy style: `--field=1,2`

对于 dict 类型:

- JSON style: `--field='{"k1": 1, "k2": 2}'`
- Environment variable style: `--field k1=1 --field k2=2`

- 混合使用: `--field k1=1,k2=2 --field k3=3 --field '{"k4": 4}'`

对于 [nested models](https://docs.pydantic.dev/2.11/concepts/models/#nested-models)，可以用如下方式传参:

```bash
python example.py \
    --v0=0 \
    --sub_model='{"v1": "json-1", "v2": "json-2"}' \
    --sub_model.v2=nested-2 \
    --sub_model.v3=3 \
    --sub_model.deep.v4=v4
```
