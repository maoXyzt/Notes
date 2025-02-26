# PG - UPDATE SET FROM

写法1（b是单表）

```sql
UPDATE a SET a.a1=b.b1,a.a2=b.b2 FROM b
WHERE b1=1 AND a1=1
```

写法2（b是子查询）

```sql
UPDATE a SET a.a1=b.b1,a.a2=b.b2 FROM (
 SELECT * FROM t
    WHERE t.id = 1
) b
WHERE b1=1 AND a1=1
```
