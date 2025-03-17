# SQL 查询每个分组的前 N 条数据

## 方法: 巧用 `row_number()` 函数

使用 `row_number()` 函数生成行号，可用行号作为条件，查询分组排序后的 N 条数据。

## 例子

查询每组排序后的第 1 条数据:

```sql
-- 每组排序后的第一条数据
SELECT * FROM (
    SELECT evnt.id AS event_id
        , row_number() over(partition by evnt.lead_id
                            order by evnt.start_time DESC, evnt.update_time DESC)
    FROM crm_event evnt
) t1
WHERE row_number = 1
```
