# SQLite 命令行客户端 LiteCLI

> <https://litecli.com/>

LiteCLI 是一个 SQLite 的命令行客户端，相对于原版 `sqlite3` 客户端，额外支持自动补全和语法高亮。

## 1 - 安装

如果有 [uv](https://github.com/astral-sh/uv) 环境，可以用 `uvx` 命令免安装使用，可略过本节。

通过 pip 安装:

```bash
pip install litecli
```

或通过 `brew` 安装

```bash
brew tap dbcli/tap
brew install litecli
```

## 2 - 使用

启动

```bash
# 借助 uvx 免安装使用:
uvx litecli <db_name>
# 安装后使用:
litecli <db_name>
```

之后会进入交互式命令行，可输入 SQL 语句查询数据库。
