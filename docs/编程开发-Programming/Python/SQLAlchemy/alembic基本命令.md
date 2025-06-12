# alembic 基本命令

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

## 2 - 生成迁移脚本

迁移脚本在 `alembic/versions` 目录下，每个脚本对应一个版本。

自动生成迁移脚本

```bash
alembic revision --autogenerate -m 'create_user_table'
```

## 3 - 根据迁移脚本，更新数据库

### 3.1 执行数据库更新命令

* `$VERSION_STR`: 可以在 `alembic/versions` 目录下找到。

```bash
alembic upgrade $VERSION_STR
alembic upgrade head    # 更新到最新版
```

### 3.2 生成数据库更新 SQL 文件

生成数据库更新文件(SQL)，用于离线

* `$SRC_VERSION`: 起始版本号
* `$TGT_VERSION`: 目标版本号

```bash
# 从数据库当前版本生成更新到目标版本的 sql
alembic upgrade $TGT_VERSION --sql > migration.sql
# 从指定版本生成更新到目标版本的 sql
alembic upgrade $SRC_VERSION:$TGT_VERSION --sql > migration.sql
```

## 4 - 其他操作

### 4.1 降级

```bash
alembic downgrade head  # 到最初版
alembic downgrade <版本号>
```

### 4.2 查看版本历史

```bash
alembic history
```
