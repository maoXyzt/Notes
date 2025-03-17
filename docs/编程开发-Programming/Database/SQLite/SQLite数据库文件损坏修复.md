# SQLite 数据库文件损坏修复

> Ref: <https://zhuanlan.zhihu.com/p/672236953>

## 问题

访问 SQLite 数据库文件时，出现如下错误信息: "database disk image is malformed."

这可能是数据库文件损坏了。

假设我们的数据库文件是 `sqlite.db`，先执行执行如下命令检查数据库文件的完整性：

```bash
sqlite3 sqlite.db "PRAGMA integrity_check;"
```

得到了类似如下的输出结果:

```text
*** in database main ***
Page 385: btreeInitPage() returns error code 11
row 920 missing from index sqlite_autoindex_history_2
row 1546 missing from index sqlite_autoindex_history_1
row 3020 missing from index sqlite_autoindex_history_2
Error: database disk image is malformed
```

说明数据库文件损坏了。

## 修复

连接数据库

```bash
sqlite3 sqlite.db
```

执行如下命令，用于导出数据库的数据:

```bash
.mode insert
.output ./dump_all.sql
.dump
.exit
```

> * `.mode insert`: 表示后续的查询结果将以插入语句的形式进行输出
> * `.output ./dump_all.sql`: 表示将查询结果或其他输出重定向到指定的文件中
> * `.dump`: 该命令将数据库的结构和内容转储为 SQL 语句，可以备份数据库或将其迁移到其他 SQLite 数据库
> * `.exit`: 退出 sqlite3

过滤 `dump_all.sql` 中的语句, 生成不含事务语句的 SQL 文件 `dump_all_notrans.sql`:

```bash
cat ./dump_all.sql | grep -v TRANSACTION | grep -v ROLLBACK | grep -v COMMIT >./dump_all_notrans.sql
```

从 `dump_all_notrans.sql` 生成修复后的数据库文件 `repair.db`

```bash
sqlite3 ./repair.db ".read ./dump_all_notrans.sql"
```
