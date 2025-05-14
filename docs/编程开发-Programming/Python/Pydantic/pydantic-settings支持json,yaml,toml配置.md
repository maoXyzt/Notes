# pydantic-settings 支持 json, yaml, toml 配置

pydantic-settings 支持从 json, yaml, toml 文件中读取配置。

## 1 - 使用方法

关键是重写 `settings_customise_sources` 方法，并返回一个包含所有配置源的元组。

```python
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

TOML_FILES = ["config.toml"]  # 配置文件路径

class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=TOML_FILES)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # the first source has the highest priority
        return (
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
            init_settings,
        )
```

Pydantic 提供如下的配置源:

- `JsonConfigSettingsSource` 使用 `json_file` 和 `json_file_encoding` 参数
- `PyprojectTomlConfigSettingsSource` 使用 `(optional) pyproject_toml_depth` 和 `(optional) pyproject_toml_table_header` 参数
- `TomlConfigSettingsSource` 使用 `toml_file` 参数
- `YamlConfigSettingsSource` 使用 `yaml_file` 和 `yaml_file_encoding` 参数

也可以继承 `PydanticBaseSettingsSource` 类，编写自定义的配置源

> <https://docs.pydantic.dev/2.11/concepts/pydantic_settings/?query=toml#adding-sources>

### 如何动态选择配置文件?

`TomlConfigSettingsSource` 等 settings source 类支持传入配置文件列表，支持多个配置文件。

可以用全局变量、环境变量等方式动态改变配置文件列表。

Example 1: 使用全局变量

```python
TOML_FILES = ["config.toml", "config.local.toml"]

class Settings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # the first source has the highest priority
        return (
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls, TOML_FILES),
            init_settings,
        )
```

Example 2: 使用环境变量

```python
class Settings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # the first source has the highest priority
        toml_files = os.environ.get("toml_config_files", "config.toml")
        return (
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls, toml_files),
            init_settings,
        )
