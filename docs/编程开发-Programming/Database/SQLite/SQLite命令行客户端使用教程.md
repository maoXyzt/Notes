# SQLite 命令行客户端使用教程

## 1 - 安装

Ubuntu / Debian 系统:

```bash
sudo apt install sqlite3 libsqlite3-dev
```

验证安装成功:

```bash
sqlite3 -version
# 输出版本号表示安装成功, 例如:
# 3.37.2 2022-01-06 13:25:41 872ba256cbf61d9290b571c0e6d82a20c224ca3ad82971edc46b29818d5dalt1
```

或者可以使用 LiteCLI 命令行客户端，参考: [SQLite 命令行客户端 LiteCLI](./SQLite命令行客户端litecli.md)

## 2 - 使用

### 2.1 查看元数据

```bash
.open <db_name>   -- 打开或创建数据库文件
.exit / .quit     -- 退出客户端
```

### 2.2 常用查询

```bash
.databases        -- 查看所有数据库
.tables           -- 查看所有表
.schema <table>   -- 查看表的SQL CREATE语句 (不带参数则查看所有表的)
.indexes <table>  -- 查看表的索引 (不带参数则查看所有表的)
```

```sql
-- 查看表结构
PRAGMA table_info(<table>);
-- 查看当前数据库页大小、编码等信息
PRAGMA page_size;
PRAGMA encoding;
PRAGMA foreign_keys;  -- 查看外键是否启用
-- 启用外键约束（默认可能关闭）
PRAGMA foreign_keys = ON;

-- 查看数据库版本
SELECT sqlite_version();
```

### 2.3 导入&导出

#### (1) `.output` 命令导出查询

导出表为 CSV 文件:

```sql
.mode csv
.output users.csv
SELECT * FROM users;
-- 恢复输出到终端
.output stdout
```

`.mode` 命令支持以下几种输出格式:

- `list` (default): 每行一条记录，字段用 \` 分隔（可通过 `.separator` 修改）
- `csv`: 字段用逗号分隔，字符串自动加双引号，符合 RFC 4180 标准
- `column`: 对齐列的表格形式 (类似 MySQL CLI), 主要用于终端可读性展示
- `table`: 使用 ASCII 表格边框 (类似 psql 的 \x 效果), 用于更美观的终端输出
- `json`: 输出为 JSON 数组 (每行为一个对象, 例如 `[{key1: value1, key2: value2}]`)（要求 SQLite ≥ 3.38.0）
- `line` / `lines`: 每个字段单独一行，格式为 字段名 = 值
- `html`: 输出为 HTML 表格
- `insert`: 输出为 `INSERT INTO table VALUES(...);` 语句, 用于数据迁移、备份还原
- `quote`: 输出为 SQL 字面量 (带引号和转义)

使用 LiteCLI 时支持更多格式，可以通过 `.mode` 命令 (不带参数) 查看。

用完 `.output` 后记得恢复输出到终端 `.output stdout`，否则后续命令的输出都会写入文件。

#### (2) `.import` 命令导入

从 CSV 文件导入数据到表:

```sql
-- 假设 users 表已存在
.separator ,    -- 设置导入/导出时的分隔符为逗号 (默认也是逗号)
.import users.csv users
```

#### (3) `.dump` 命令备份数据库

用于备份整个数据库

在 shell 中直接备份:

```bash
sqlite3 mydb.db .dump > backup.sql
```

在客户端中备份:

```sql
.output backup.sql
.dump
-- 恢复输出到终端
.output stdout
```
