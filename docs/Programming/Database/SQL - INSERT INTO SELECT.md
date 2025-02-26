# SQL - INSERT INTO SELECT

```sql
INSERT INTO table2
(col_a, col_b)
SELECT aaa, bbb
FROM table1;
```

当select的结果有多行时，插入的数据也有多行。
