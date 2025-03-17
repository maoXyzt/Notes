# SQL 批量从 A 表插入数据到 B 表

INSERT FROM 语句: 把 table1 的数据批量插入 table2:

```sql
INSERT INTO table2
(col_a, col_b)
SELECT aaa, bbb
FROM table1;
```

当 `SELECT` 的结果有多行时，插入的数据也有多行。
