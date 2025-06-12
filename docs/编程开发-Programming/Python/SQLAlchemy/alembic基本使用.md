# alembic 基本使用

[alembic](https://github.com/sqlalchemy/alembic) 是 SQLAlchemy 的迁移工具。

## 1 - 安装与初始化

```bash
pip install alembic
```

初始化迁移目录

```bash
alembic init alembic
```

目录结构类似:

```bash
yourproject/
    alembic.ini
    pyproject.toml
    alembic/
        env.py
        README
        script.py.mako
        versions/
            3512b954651e_add_account.py
            2b1ae634e5cd_add_order_id.py
            3adcc9a56557_rename_username_field.py
```

* `alembic.ini` - Alembic 的主配置文件，由所有模板生成。
* `env.py` - 这是一个 Python 脚本，每当调用 alembic 迁移工具时都会运行。
  * 它至少包含配置和生成 SQLAlchemy 引擎的指令，从该引擎获取连接和事务，然后调用迁移引擎，使用该连接作为数据库连接的源。
  * `env.py` 脚本是生成环境的一部分，因此迁移的运行方式是完全可自定义的。这里包含了如何连接的具体细节，以及如何调用迁移环境的具体细节。
  * 可以修改脚本以操作多个引擎，可以将自定义参数传递到迁移环境中，可以加载并使应用程序特定的库和模型可用。
* `script.py.mako` - 这是一个 Mako 模板文件，用于生成新的迁移脚本。
* `versions` - 迁移脚本目录，每个脚本对应一个版本。

## 2 - 配置

### 2.1 配置文件 `alembic.ini`

> [Editing the .ini File](https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file)

### 2.2 配置文件 `pyproject.toml`

从 `alembic>=1.16.0` 开始，可以使用 `pyproject.toml` 配置 Alembic。

> [Using pyproject.toml for configuration](https://alembic.sqlalchemy.org/en/latest/tutorial.html#using-pyproject-toml-for-configuration)

使用如下命令初始化迁移目录，并在 `pyproject.toml` 中添加 Alembic 配置:

```bash
alembic init --template pyproject alembic
```

此时，`alembic.ini` 文件只包含数据库连接配置和 logging 配置。

如果在 `env.py` 文件中配置了数据库连接和 logging 配置，则可以省略 `alembic.ini` 文件。

## 3 - 生成迁移脚本

迁移脚本在 `alembic/versions` 目录下，每个脚本对应一个版本。

自动生成迁移脚本

```bash
alembic revision --autogenerate -m 'create_user_table'
```

## 4 - 根据迁移脚本，更新数据库

### 4.1 执行数据库更新命令

* `$VERSION_STR`: 可以在 `alembic/versions` 目录下找到。

```bash
alembic upgrade $VERSION_STR
alembic upgrade head    # 更新到最新版
```

### 4.2 生成数据库更新 SQL 文件

生成数据库更新文件(SQL)，用于离线

* `$SRC_VERSION`: 起始版本号
* `$TGT_VERSION`: 目标版本号

```bash
# 从数据库当前版本生成更新到目标版本的 sql
alembic upgrade $TGT_VERSION --sql > migration.sql
# 从指定版本生成更新到目标版本的 sql
alembic upgrade $SRC_VERSION:$TGT_VERSION --sql > migration.sql
```

## 5 - 其他操作

### 5.1 降级

```bash
alembic downgrade head  # 到最初版
alembic downgrade <版本号>
```

### 5.2 查看版本历史

```bash
alembic history
```
