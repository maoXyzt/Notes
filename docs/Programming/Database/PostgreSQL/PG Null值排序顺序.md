# PG Null 值排序顺序

> Ref：<https://blog.csdn.net/weixin_42183854/article/details/83650624>

`null` 排在有值的行前面还是后面通过语法来指定

```sql
--null 值在前
SELECT * FROM tablename ORDER BY id nulls first;

--null 值在后
SELECT * FROM tablename ORDER BY id nulls last;

--null 在前配合 desc 使用
SELECT * FROM tablename ORDER BY id desc nulls first;

--null 在后配合 desc 使用
SELECT * FROM tablename ORDER BY id desc nulls last;
```

例如：

```sql
-- null 值在后, 先按照 count1 降序排列, count1 相同再按照 count2 降序排列
SELECT * FROM tablename
ORDER BY count1 desc nulls last, count2 desc nulls last;
```
